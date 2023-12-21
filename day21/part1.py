#!/usr/bin/env python3

import argparse
import sys

parser = argparse.ArgumentParser()
parser.add_argument("--input", "-i", default=sys.stdin, type=argparse.FileType("r"))
parser.add_argument("--steps", "-s", default=6, type=int)
args = parser.parse_args()

class Node:
    def __init__(self, value):
        self.value = value
        self.visited = False
        self.stop = False

grid = [ [ Node(char) for char in line.strip() ] for line in args.input.readlines() ]

for j in range(len(grid)):
    for i in range(len(grid[j])):
        if grid[j][i].value == "S":
            x, y = i, j
            break

processing = [ (x, y, args.steps) ]
while len(processing) > 0:
    (x, y, steps) = processing.pop(0)
    if grid[y][x].visited:
        continue
    grid[y][x].visited = True
    if steps % 2 == 0:
        grid[y][x].stop = True
    if steps == 0:
        continue
    if x > 0 and grid[y][x-1].value != "#" and not grid[y][x-1].visited:
        processing.append((x-1, y, steps-1))
    if y > 0 and grid[y-1][x].value != "#" and not grid[y-1][x].visited:
        processing.append((x, y-1, steps-1))
    if x < len(grid[y])-1 and grid[y][x+1].value != "#" and not grid[y][x+1].visited:
        processing.append((x+1, y, steps-1))
    if y < len(grid)-1 and grid[y+1][x].value != "#" and not grid[y+1][x].visited:
        processing.append((x, y+1, steps-1))

total = 0
for row in grid:
    for node in row:
        if node.stop:
            total += 1
print("Total:", total)
