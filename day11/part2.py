#!/usr/bin/env python3

import argparse
import sys

parser = argparse.ArgumentParser()
parser.add_argument("--input", "-i", default=sys.stdin, type=argparse.FileType("r"))
parser.add_argument("--increment", default=1000000, type=int)
args = parser.parse_args()

grid = []
for line in args.input.readlines():
    row = []
    for char in line.strip():
        row.append(char)
    grid.append(row)
columns = [ 0 for i in range(len(grid)) ]
rows = [ 0 for j in range(len(grid[0])) ]
for i in range(len(grid)):
    for j in range(len(grid[i])):
        if grid[j][i] == ".":
            rows[j] += 1
            columns[i] += 1
for i in range(len(rows)):
    rows[i] = rows[i] == len(columns)
for j in range(len(columns)):
    columns[j] = columns[j] == len(rows)
for j in range(len(grid)):
    for i in range(len(grid[j])):
        if rows[j] or columns[i]:
            grid[j][i] = "X"
galaxies = []
for j in range(len(grid)):
    for i in range(len(grid[j])):
        if grid[j][i] == "#":
            galaxies.append((i, j))
total = 0
for i in range(len(galaxies)):
    for j in range(i+1, len(galaxies)):
        if i == j:
            continue
        (a, b) = galaxies[i]
        (c, d) = galaxies[j]
        if a <= c:
            x_increment = 1
        else:
            x_increment = -1
        if b <= d:
            y_increment = 1
        else:
            y_increment = -1
        for x in range(a, c, x_increment):
            if grid[b][x] == "X":
                total += args.increment
            else:
                total += 1
        for y in range(b, d, y_increment):
            if grid[y][a] == "X":
                total += args.increment
            else:
                total += 1
print("Total:", total)
