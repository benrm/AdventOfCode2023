#!/usr/bin/env python3

import argparse
import sys

parser = argparse.ArgumentParser()
parser.add_argument("--input", "-i", default=sys.stdin, type=argparse.FileType("r"))
args = parser.parse_args()

class Node:
    def __init__(self, char):
        self.char = char
        self.north = None
        self.east = None
        self.south = None
        self.west = None
        self.previous = None
        self.next = None

    def __str__(self):
        directions = []
        if self.north is not None:
            directions.append("North")
        if self.east is not None:
            directions.append("East")
        if self.south is not None:
            directions.append("South")
        if self.west is not None:
            directions.append("West")
        return "Node(" + ", ".join(directions) + ")"

    def __repr__(self):
        return self.__str__()

start = None
grid = []
for line in args.input.readlines():
    row = []
    for char in line:
        if char == "\n":
            break
        node = Node(char)
        if node.char == "S":
            start = node
        row.append(node)
    grid.append(row)

for y in range(len(grid)):
    for x in range(len(grid[y])):
        node = grid[y][x]
        if (node.char == "|" or node.char == "J" or node.char == "L") and y > 0: # North
            node.north = grid[y-1][x]
        if (node.char == "-" or node.char == "L" or node.char == "F") and x < len(grid[y])-1: # East
            node.east = grid[y][x+1]
        if (node.char == "|" or node.char == "7" or node.char == "F") and y < len(grid)-1: # South
            node.south = grid[y+1][x]
        if (node.char == "-" or node.char == "J" or node.char == "7") and x > 0: # West
            node.west = grid[y][x-1]
        if node.char == "S":
            if y > 0:
                north = grid[y-1][x]
                if north.char == "|" or north.char == "7" or north.char == "F":
                    node.north = north
            if x < len(grid[y])-1:
                east = grid[y][x+1]
                if east.char == "-" or east.char == "J" or east.char == "7":
                    node.east = east
            if y < len(grid)-1:
                south = grid[y+1][x]
                if south.char == "|" or south.char == "L" or south.char == "J":
                    node.south = south
            if x > 0:
                west = grid[y][x-1]
                if west.char == "-" or west.char == "L" or west.char == "F":
                    node.west = west
            if node.north is not None and node.east is not None:
                node.char = "L"
            elif node.north is not None and node.south is not None:
                node.char = "|"
            elif node.north is not None and node.west is not None:
                node.char = "J"
            elif node.east is not None and node.south is not None:
                node.char = "F"
            elif node.east is not None and node.west is not None:
                node.char = "-"
            elif node.south is not None and node.west is not None:
                node.char = "7"
            else:
                raise Exception("Start node is not a known type: {node}")

if start.north is not None:
    start.previous = start.north
elif start.east is not None:
    start.previous = start.east
elif start.south is not None:
    start.previous = start.south
elif start.west is not None:
    start.previous = start.west
else:
    raise Exception(f"Start node has no neighbors")

is_start = True
current = start
while current != start or is_start:
    is_start = False
    if current.north is not None and current.north.south is not None and current.previous != current.north:
        current.next = current.north
    elif current.east is not None and current.east.west is not None and current.previous != current.east:
        current.next = current.east
    elif current.south is not None and current.south.north is not None and current.previous != current.south:
        current.next = current.south
    elif current.west is not None and current.west.east is not None and current.previous != current.west:
        current.next = current.west
    else:
        raise Exception(f"Node has no neighbors not visited: {current}")
    current.next.previous = current
    current = current.next

enclosed = 0
for row in grid:
    outside = True
    start = None
    for node in row:
        if node.previous is None:
            if not outside:
                enclosed += 1
        else:
            if node.char == "F" or node.char == "L":
                start = node.char
            elif node.char == "|":
                outside = not outside
            elif node.char == "7" and start == "L":
                outside = not outside
            elif node.char == "J" and start == "F":
                outside = not outside
print("Enclosed:", enclosed)
