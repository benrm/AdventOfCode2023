#!/usr/bin/env python3 

import argparse
import math
import re
import sys

parser = argparse.ArgumentParser()
parser.add_argument("--input", "-i", default=sys.stdin, type=argparse.FileType("r"))
args = parser.parse_args()

directions = args.input.readline().strip()

args.input.readline()

line_re = re.compile("(\w+)\s+=\s+\((\w+),\s+(\w+)\)")
a_re = re.compile(".*[Aa]$")
z_re = re.compile(".*[Zz]$")

nodes = {}
for line in args.input.readlines():
    matches = line_re.match(line)
    if not matches:
        raise Exception(f"Non-matching line: {line}")
    nodes[matches[1]] = { "L": matches[2], "R": matches[3] }

start_nodes = set()
for node in nodes:
    matches = a_re.match(node)
    if matches:
        start_nodes.add(node)

finishes = []
for node in start_nodes:
    i = 0
    count = 0
    current = node
    while True:
        current = nodes[current][directions[i]]
        i = (i + 1) % len(directions)
        count += 1
        matches = z_re.match(current)
        if matches:
            finishes.append(count)
            break
print("LCM:", math.lcm(*finishes))
