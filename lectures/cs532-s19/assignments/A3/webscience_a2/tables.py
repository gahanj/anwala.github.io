import json

data = json.load(open("urlsClean.json"))

for url in data:
    try:
        x = data[url]["keywords"]["Mueller"]["Alexa-global"]
        print("%d ~ %s" % (data[url]["keywords"]["Mueller"]["PR"], url ))
    except KeyError as e:
        pass