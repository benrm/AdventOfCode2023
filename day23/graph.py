#!/usr/bin/env python3

import argparse
import pydot
import sys

parser = argparse.ArgumentParser()
parser.add_argument("--input", "-i", default=sys.stdin, type=argparse.FileType("r"))
parser.add_argument("--output", "-o", default="graph.png")
args = parser.parse_args()

class Square:
    def __init__(self, x, y, value):
        self.x = x
        self.y = y
        self.value = value
        self.id = None
        self.is_node = False
        self.visited = False

    def __str__(self):
        return f"Square(x={self.x},y={self.y},value={self.value})"

    def __repr__(self):
        return self.__str__()

lines = [ line.strip() for line in args.input.readlines() ]
grid = []
for y in range(len(lines)):
    row = []
    for x in range(len(lines[y])):
        row.append(Square(x, y, lines[y][x]))
    grid.append(row)

_id = 0
intersections = {}
for y in range(len(grid)):
    for x in range(len(grid[y])):
        if grid[y][x].value == "#":
            continue
        connections = 0
        if y > 0 and grid[y-1][x].value != "#":
            connections += 1
        if x < len(grid[y])-1 and grid[y][x+1].value != "#":
            connections += 1
        if y < len(grid)-1 and grid[y+1][x].value != "#":
            connections += 1
        if x > 0 and grid[y][x-1].value != "#":
            connections += 1
        if connections > 2:
            intersections[str(_id)] = grid[y][x]
            intersections[str(_id)].is_node = True
            intersections[str(_id)].id = str(_id)
            _id += 1

for x in range(len(grid[0])):
    if grid[0][x].value == ".":
        intersections["start"] = grid[0][x]
        intersections["start"].id = "start"
        intersections["start"].is_node = True
        break

for x in range(len(grid[len(grid)-1])):
    if grid[len(grid)-1][x].value == ".":
        intersections["end"] = grid[len(grid)-1][x]
        intersections["end"].id = "end"
        intersections["end"].is_node = True
        break

class Node:
    def __init__(self, _id):
        self.id = _id
        self.edges = {}

    def __str__(self):
        return f"Node(id={self.id},edges={self.edges})"

nodes = { _id: Node(_id) for _id in intersections }
for _id in intersections:
    processing = [ (intersections[_id], 0) ]
    while len(processing) > 0:
        (current, steps) = processing.pop(0)
        if steps > 0 and current.is_node:
            nodes[_id].edges[current.id] = steps
            nodes[current.id].edges[_id] = steps
            continue
        current.visited = True
        x, y = current.x, current.y
        if y > 0 and grid[y-1][x].value != "#" and not grid[y-1][x].visited:
            processing.append((grid[y-1][x], steps+1))
        if x < len(grid[y])-1 and grid[y][x+1].value != "#" and not grid[y][x+1].visited:
            processing.append((grid[y][x+1], steps+1))
        if y < len(grid)-1 and grid[y+1][x].value != "#" and not grid[y+1][x].visited:
            processing.append((grid[y+1][x], steps+1))
        if x > 0 and grid[y][x-1].value != "#" and not grid[y][x-1].visited:
            processing.append((grid[y][x-1], steps+1))

graph = pydot.Dot("Hike Graph")

added = set()
for _id in nodes:
    for edge in nodes[_id].edges:
        if edge not in added:
            graph.add_edge(pydot.Edge(_id, edge, dir="both", label=nodes[_id].edges[edge]))
    added.add(_id)

graph.write_png(args.output)
