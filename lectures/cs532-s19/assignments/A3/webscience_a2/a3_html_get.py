import requests
import json
import sys
from boilerpipe.extract import Extractor

data = json.load(open("urlsClean.json"))
count = 0

for url in data:
    count += 1
    try:
        html = requests.get(url, timeout=15)
        md5 = hash(str(url).strip()) + sys.maxsize  # we has sys.maxsize here so we don't produce negative nums as hash
        with open("./rawhtml/%s.html" % md5, 'w') as outFile:
            outFile.write(html.text)

        extractor = Extractor(html=html.text)
        with open("./texthtml/%s.txt" % md5, 'w') as outFile:
            outFile.write(extractor.getText())

        data[url]['%s' % "html_raw_filename"] = "%s.html" % md5
        data[url]['%s' % "html_text_filename"] = "%s.txt" % md5
    except Exception as e:
        print("Error:", str(e), ":  %s" % url)
        with open('a3_html_get_ErrorURLs.txt', 'a') as err:
            err.write("%s\n" % url)
    if count % 50 == 0:
        print("%d Links have been processed" % count)

# rewrite urlsClean.json with new html file names
with open('urlsClean.json', 'w')as outFile:
    pretty_data = json.dumps(data, indent=4)
    outFile.write(pretty_data)