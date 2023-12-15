#!/usr/bin/env python3

import argparse
import sys

parser = argparse.ArgumentParser()
parser.add_argument("--input", "-i", default=sys.stdin, type=argparse.FileType("r"))
args = parser.parse_args()

grid = [ [ char for char in line.strip() ] for line in args.input.readlines() ]

def fingerprint(grid):
    f = 0
    for row in grid:
        for char in row:
            f = f << 1 
            if char == "O":
                f = f | 1
    return f

def cycle(grid):
    moved = True
    while moved:
        moved = False
        for y in range(len(grid)):
            for x in range(len(grid[y])):
                if grid[y][x] == "O" and y > 0 and grid[y-1][x] == ".":
                    grid[y-1][x] = "O"
                    grid[y][x] = "."
                    moved = True
    moved = True
    while moved:
        moved = False
        for y in range(len(grid)):
            for x in range(len(grid[y])):
                if grid[y][x] == "O" and x > 0 and grid[y][x-1] == ".":
                    grid[y][x-1] = "O"
                    grid[y][x] = "."
                    moved = True
    moved = True
    while moved:
        moved = False
        for y in range(len(grid)):
            for x in range(len(grid[y])):
                if grid[y][x] == "O" and y < len(grid)-1 and grid[y+1][x] == ".":
                    grid[y+1][x] = "O"
                    grid[y][x] = "."
                    moved = True
    moved = True
    while moved:
        moved = False
        for y in range(len(grid)):
            for x in range(len(grid[y])):
                if grid[y][x] == "O" and x < len(grid[y])-1 and grid[y][x+1] == ".":
                    grid[y][x+1] = "O"
                    grid[y][x] = "."
                    moved = True
    return grid

def total_load(grid):
    length = len(grid)
    total = 0
    for y in range(len(grid)):
        for char in grid[y]:
            if char == "O":
                total += length - y
    return total

visited = {}
i = 0
while fingerprint(grid) not in visited:
    visited[fingerprint(grid)] = i
    grid = cycle(grid)
    i += 1

cycle_length = i - visited[fingerprint(grid)]

i = (1000000000 - visited[fingerprint(grid)]) // cycle_length * cycle_length + visited[fingerprint(grid)]
while i < 1000000000:
    grid = cycle(grid)
    i += 1

print("Total:", total_load(grid))
