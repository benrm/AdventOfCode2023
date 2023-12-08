#!/usr/bin/env python3 

import argparse
import re
import sys

parser = argparse.ArgumentParser()
parser.add_argument("--input", "-i", default=sys.stdin, type=argparse.FileType("r"))
args = parser.parse_args()

directions = args.input.readline().strip()

args.input.readline()

line_re = re.compile("(\w+)\s+=\s+\((\w+),\s+(\w+)\)")

nodes = {}
for line in args.input.readlines():
    matches = line_re.match(line)
    if not matches:
        raise Exception(f"Non-matching line: {line}")
    nodes[matches[1]] = { "L": matches[2], "R": matches[3] }

current = "AAA"
i = 0
count = 0
while current != "ZZZ":
    current = nodes[current][directions[i]]
    i = (i + 1) % len(directions)
    count += 1
print("Count:", count)
