#!/usr/bin/env python3

import argparse
import sys

parser = argparse.ArgumentParser()
parser.add_argument("--input", "-i", default=sys.stdin, type=argparse.FileType("r"))
args = parser.parse_args()

grid = [ [ char for char in line.strip() ] for line in args.input.readlines() ]

moved = True
while moved:
    moved = False
    for y in range(len(grid)):
        for x in range(len(grid[y])):
            if grid[y][x] == "O" and y > 0 and grid[y-1][x] == ".":
                grid[y-1][x] = "O"
                grid[y][x] = "."
                moved = True

length = len(grid)
total = 0
for y in range(len(grid)):
    for char in grid[y]:
        if char == "O":
            total += length - y
print("Total:", total)
