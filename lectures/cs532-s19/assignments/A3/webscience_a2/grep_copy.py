import json
from shutil import copy2
import os


os.system("grep -R -l \"Mueller\" ./texthtml > grep.txt")
goodURL = json.load(open("urlsClean.json"))


with open("./grep.txt", 'r') as grepped:
    for line in grepped:
        file = grepped.readline()
        file = file.strip()
        try:
            urlCleanSearch = (file.split("/"))[2]
        except IndexError as e:
            print(str(e))
            continue
        #print(urlCleanSearch)
        for url in goodURL:
            try:
                if goodURL[url]["html_text_filename"] == urlCleanSearch:
                    goodURL[url]["keywords"] = {}
                    goodURL[url]["keywords"]["Mueller"] = {}
                    #print(goodURL[url])
            except Exception as e:
                pass
        print(file)
        copy2(file, './tenURLs')


# rewrite urlsClean.json with new html file names
with open('urlsClean.json', 'w')as outFile:
    pretty_data = json.dumps(goodURL, indent=4)
    outFile.write(pretty_data)


