import matplotlib.pyplot as plt
import numpy as np
import json
import pandas as pd
from scipy import stats
from statistics import mode
from pylab import *

data = []
with open("./acnwala-friendscount.csv", 'r') as inFile:
    for line in inFile:
        number = int((line.split(","))[1])
        name = line.split(",")[0]
        data.append([number,name])

print(data)
data.sort()
print(data)
numbers = []
for i in range(0,len(data) - 1):
    numbers.append(data[i][0])
print(numbers)

sdev = np.std(numbers)
print(sdev)
mean = np.mean(numbers)
print(mean)
mode_ = mode(numbers)
print(mode_)
median = np.median(numbers)
print(median)
anwala = len(numbers)

t = arange(0, 97)
plt.plot(t, numbers)
xlabel = ("Nwala's Friends")
ylabel = ("NWala's Friend's # of Friends")
title("Chart 1: Nwala's Friend count vs Nwala's Friend's Friends count")
grid(True)

manual_nums = [anwala,median,mean,sdev]
y_coord = [15,35,55,75]
manual_entries = ["Nwala 98", "Median 395",  "Mean 507", "SDEV 411"]

for i,manual_entries in enumerate(manual_entries):
    x = manual_nums[i]
    y = y_coord[i]
    plt.scatter(y,x, marker='x', color='red')
    plt.text(y, x+80, manual_entries, fontsize=9)
plt.tight_layout()
plt.show()

