import matplotlib.pyplot as plt
import numpy as np
import json
import datetime
import time
import dateutil.parser


def addPlotData(x,y,timeDiff,mementCount):
    x.append(timeDiff)
    y.append(mementCount)

data = json.load(open("urlsClean.json"))

plot = []
x = []
y = []

for uri in data:
    mement = data[uri]["momentos"]
    if mement > 0 and len(data[uri]["carbonDate"]) > 1 and mement < 50:
        date = dateutil.parser.parse(data[uri]["carbonDate"])
        now = datetime.datetime.now()
        delta = (now - date).days
        addPlotData(x,y,delta,mement)

print(sorted(y))

plot = plt.scatter(x,y,facecolors='none', edgecolors='r', alpha=0.5)
plt.xlabel("Age")
plt.ylabel("Memento Count")
plt.title("Estimated Age vs Memento Count")
plt.show()