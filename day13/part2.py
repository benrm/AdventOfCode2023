#!/usr/bin/env python3

import argparse
import sys

parser = argparse.ArgumentParser()
parser.add_argument("--input", "-i", default=sys.stdin, type=argparse.FileType("r"))
args = parser.parse_args()

grids = []
grid = []
for line in [ line.strip() for line in args.input.readlines() ]:
    row = [ char for char in line ]
    if len(row) == 0:
        grids.append(grid)
        grid = []
    else:
        grid.append(row)
grids.append(grid)

def find_vertical_reflection(grid):
    for i in range(1, len(grid[0])):
        is_reflection = True
        j = i
        k = i - 1
        while j < len(grid[0]) and k >= 0:
            for y in range(len(grid)):
                if grid[y][k] != grid[y][j]:
                    is_reflection = False
                    break
            if not is_reflection:
                break
            j += 1
            k -= 1
        if is_reflection:
            return i
    return 0

def find_smudged_vertical_reflection(grid):
    vertical_reflection = find_vertical_reflection(grid)
    for i in range(1, len(grid[0])):
        if i == vertical_reflection:
            continue
        errors = 0
        j = i
        k = i - 1
        while j < len(grid[0]) and k >= 0:
            for y in range(len(grid)):
                if grid[y][k] != grid[y][j]:
                    errors += 1
                if errors > 1:
                    break
            if errors > 1:
                break
            j += 1
            k -= 1
        if errors == 1:
            return i
    return 0

total = 0
for i in range(len(grids)):
    vertical_reflection = find_smudged_vertical_reflection(grids[i])
    horizontal_reflection = find_smudged_vertical_reflection([ [ grids[i][x][y] for x in range(len(grids[i])) ] for y in range(len(grids[i][0])) ])
    total += vertical_reflection + horizontal_reflection * 100
print("Total:", total)
