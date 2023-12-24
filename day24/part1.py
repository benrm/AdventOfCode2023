#!/usr/bin/env python3

import argparse
import re
import sys

parser = argparse.ArgumentParser()
parser.add_argument("--input", "-i", default=sys.stdin, type=argparse.FileType("r"))
parser.add_argument("--min", default=200000000000000, type=int)
parser.add_argument("--max", default=400000000000000, type=int)
args = parser.parse_args()

class Hail:
    def __init__(self, px, py, vx, vy):
        self.px = px
        self.py = py
        self.vx = vx
        self.vy = vy
        self.slope = vy/vx
        self.intercept = -1 * vy / vx * px + py

    def __str__(self):
        return f"Hail(px={self.px},py={self.py},vx={self.vx},vy={self.vy},slope={self.slope},intercept={self.intercept})"

hail_re = re.compile("(-?\d+),\s*(-?\d+),\s*-?\d+\s*@\s*(-?\d+),\s*(-?\d+)")

hail = []
for line in args.input.readlines():
    matches = hail_re.match(line)
    if not matches:
        raise Exception(f"Non-matching line: {line}")
    hail.append(Hail(float(matches[1]), float(matches[2]), float(matches[3]), float(matches[4])))

total = 0
for i in range(len(hail)):
    for j in range(i+1,len(hail)):
        if i != j and hail[i].slope != hail[j].slope:
            x = (hail[i].intercept - hail[j].intercept)/(hail[j].slope - hail[i].slope)
            y = hail[i].slope * x + hail[i].intercept
            ti = (x - hail[i].px) / hail[i].vx
            tj = (x - hail[j].px) / hail[j].vx
            if args.min <= x and args.max >= x and args.min <= y and args.max >= y and ti > 0 and tj > 0:
                total += 1
print("Total:", total)
