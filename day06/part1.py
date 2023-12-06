#!/usr/bin/env python3

import argparse
import math
import re
import sys

parser = argparse.ArgumentParser()
parser.add_argument("--input", "-i", default=sys.stdin, type=argparse.FileType("r"))
args = parser.parse_args()

number_re = re.compile("\d+")

lines = args.input.readlines()
times = number_re.findall(lines[0])
distances = number_re.findall(lines[1])
if len(times) != len(distances):
    raise Exception(f"Have {len(times)} times and {len(distances)} distances")
races = [ (int(times[i]), int(distances[i])) for i in range(len(times)) ]

product = 1
for race in races:
    (time, distance) = race
    _min = (time - math.sqrt(time**2 - 4 * distance))/2
    _ceil = math.ceil(_min)
    if _min == _ceil:
        _min += 1
    else:
        _min = _ceil
    _max = (time + math.sqrt(time**2 - 4 * distance))/2
    _floor = math.floor(_max)
    if _max == _floor:
        _max -= 1
    else:
        _max = _floor
    print(f"Time: {time}; Distance: {distance}; Min: {_min}; Max: {_max}")
    product *= _max - _min + 1
print("Product:", product)
