import threading
import datetime
import numpy as np


time = 0
buses = {}

with open("data.txt", "r") as file:
    buses = {int(x): i for i, x in enumerate(file.readline().strip().split(",")) if x != "x"}
    keys = list(buses.keys())




def check(i, num):
    for k in keys[:i + 1]:
        if (num + buses[k]) % k != 0:
            return False
    return True

def solve():
    num = 0
    add = keys[0]
    for i in range(1, len(buses)):
        while True:
            if check(i, num):
                arr = np.array(keys[:i + 1])
                add = np.lcm.reduce(arr)
                break
            num += add
    return num
    

num = solve()
for key in buses:
    print(key, buses[key], (num + buses[key]) % key)
