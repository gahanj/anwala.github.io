import json
import sys
import requests
import time

if len(sys.argv) < 2:
    print("Invalid arguments. Usage: momentosGet.py {memgator_url}")
    sys.exit(1)
else:
    try:
        res = requests.get(sys.argv[1])
        print('memgator url: %s' % res.url)
    except:
        print("memgator url is not valid")
        sys.exit(1)


memgator_url = sys.argv[1]
# create backup of URL database file
backup = json.load(open("urlsClean.json"))
with open('urlsClean.bak', 'w') as json_file:
    json.dump(backup, json_file)
    json_file.close()

with open('urlsClean.json', 'r+') as url_db:
    urls_to_Momentize = json.load(url_db)
    count = 0
    momento_count = 0
    for url in urls_to_Momentize:
        if urls_to_Momentize[url]["momentos"] <= 0:
            count += 1
            try:
                res = requests.get("%s/timemap/json/%s" % (memgator_url, url))
                if(res.status_code == 200 or res.status_code == 302):
                    try:
                        urls_to_Momentize[url]["momentos"] = res.headers['X-Memento-Count']
                        momento_count += int(res.headers['X-Memento-Count'])
                        if urls_to_Momentize[url]["timeMapFilename"] == " ":
                            timeMapFileName = "%d.txt" % abs(hash(url))
                        else:
                            timeMapFileName = urls_to_Momentize[url]["timeMapFilename"]
                        with open("./timemaps/%s" % timeMapFileName, 'w') as outFile:
                            outFile.write(res.text)
                        urls_to_Momentize[url]["timeMapFilename"] = timeMapFileName
                    except Exception as e:
                        print("Error: ", str(e))

                time.sleep(0.5)
            except Exception as e:
                print("Error occured sending url to memgator" + " :: " + url + str(e))

            if count % 5 == 0:
                print("%d links passed to memgator.  %d total momentos found" % (count, momento_count))
    #writing to db
    pretty_data = json.dumps(urls_to_Momentize, indent=4)
    url_db.write(pretty_data)