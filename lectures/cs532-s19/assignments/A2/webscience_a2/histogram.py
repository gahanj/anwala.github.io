import matplotlib.pyplot as plt
import numpy as np
import json
import pandas as pd


def addTuple(x,y):
    return [x,y]

data = json.load(open("urlsClean.json"))

momento_count = {}


for uri, uriDCT in data.items():

    momento_count.setdefault(uriDCT['momentos'],0)
    momento_count[uriDCT['momentos']] += 1


momento_count = list(momento_count.items())
momento_count.sort(key=lambda x: x[0])

x = []
for item in momento_count:
    x.append(item[0])

y = []
for item in momento_count:
    y.append(item[1])

z = 231
plot = []
plot.append(addTuple(x[25], 0))
plot.append(addTuple(x[20], 0))
plot.append(addTuple(x[15], 0))
plot.append(addTuple(x[10], 0))
plot.append(addTuple(x[3], 0))
plot.append(addTuple(x[2], 0))
plot.append(addTuple(x[1], 0))
plot.append(addTuple(x[0], 0))
while z >=  0:
    if z >= 25:
        plot[0][1] += y[z]
        z -= 1
    elif z >= 20:
        plot[1][1] += y[z]
        z -= 1
    elif z >= 15:
        plot[2][1] += y[z]
        z -= 1
    elif z >= 10:
        plot[3][1] += y[z]
        z -= 1
    elif z >= 3:
        plot[4][1] += y[z]
        z -= 1
    elif z == 2:
        plot[5][1] += y[z]
        z -= 1
    elif z == 1:
        plot[6][1] += y[z]
        z -= 1
    elif z == 0:
        plot[7][1] += y[z]
        z -= 1

plot.sort(key=lambda x: x[0])


x = []
y = []

for item in plot:
    x.append(item[0])
    y.append(item[1])

print("reduced Data set:" ,plot)
print("x from reduced data set: " ,x)
print("y from reduced data set: " ,y)

bars = plt.bar([0,1,2,3,4,5,6,7],y,width=0.7)

# https://stackoverflow.com/questions/40489821/how-to-write-text-above-the-bars-on-a-bar-plot-python
for rect in bars:
    height = rect.get_height()
    plt.text(rect.get_x() + rect.get_width()/2.0, height + 20, '%d' % int(height), ha='center', va="bottom" )


labels = ['0','1','2','3-9','10-14','15-19','20-24','25+']
plt.xticks([0,1,2,3,4,5,6,7],labels=labels)
plt.xlabel("Memento Count")
plt.ylabel("Frequency")
plt.title("Frequency of urls with given memento count")
plt.show()

