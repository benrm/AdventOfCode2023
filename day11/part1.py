#!/usr/bin/env python3

import argparse
import sys

parser = argparse.ArgumentParser()
parser.add_argument("--input", "-i", default=sys.stdin, type=argparse.FileType("r"))
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
tmp = []
for j in range(len(rows)):
    tmp.append(grid[j])
    if rows[j]:
        tmp.append(["."] * len(rows))
grid = tmp
tmp = [ [ grid[i][j] for i in range(len(grid)) ] for j in range(len(grid[0])) ]
grid = tmp
tmp = []
for i in range(len(columns)):
    tmp.append(grid[i])
    if columns[i]:
        tmp.append(["."] * len(grid[0]))
grid = tmp
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
        total += abs(d-b) + abs(c-a)
print("Total:", total)
