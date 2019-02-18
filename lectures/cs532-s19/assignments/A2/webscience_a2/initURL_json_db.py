#!/usr/bin/python3/

import json

def initializeURLJSON():
    # create backup of URL database file
    backup = json.load(open("urlsClean.json"))
    with open('urlsClean.bak', 'w') as json_file:
        json.dump(backup, json_file)
        json_file.close()

    # reopen file and get count of URLS present. Store data in goodURL and count in goodURLCount
    goodURL = json.load(open("urlsClean.json"))

    with open('parsedURLs.txt', 'r') as urls:
        for line in urls:
            outUrl = line.strip()
            goodURL["%s" % outUrl] = {"momentos": 0, "timeMapFilename": " ", "carbonDate": " "}

    with open('urlsClean.json', 'w')as outFile:
        pretty_data = json.dumps(goodURL, indent=4)
        outFile.write(pretty_data)


initializeURLJSON()