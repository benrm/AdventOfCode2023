#!/usr/bin/env python3

import argparse
import sys

parser = argparse.ArgumentParser()
parser.add_argument("--input", "-i", default=sys.stdin, type=argparse.FileType("r"))
args = parser.parse_args()

max_x = 0
max_y = 0
min_x = 0
min_y = 0

x = 0
y = 0

commands = []
for line in args.input.readlines():
    words = line.split()
    direction = words[0]
    distance = int(words[1])
    if direction == "U":
        y += distance
        if y > max_y:
            max_y = y
    elif direction == "R":
        x += distance
        if x > max_x:
            max_x = x
    elif direction == "D":
        y -= distance
        if y < min_y:
            min_y = y
    elif direction == "L":
        x -= distance
        if x < min_x:
            min_x = x
    commands.append((direction, distance))

x_offset = -1 * min_x
y_offset = -1 * min_y

grid = [ [ None for x in range(min_x, max_x + 1, 1) ] for y in range(min_y, max_y + 1, 1) ]

x = 0
y = 0

class Node:
    def __init__(self, up=None, right=None, down=None, left=None):
        self.up = up
        self.right = right
        self.down = down
        self.left = left

    def __str__(self):
        neighbors = []
        if self.up is not None:
            neighbors.append("up")
        if self.right is not None:
            neighbors.append("right")
        if self.down is not None:
            neighbors.append("down")
        if self.left is not None:
            neighbors.append("left")
        return "Node(neighbors=" + ",".join(neighbors) + ")"

    def __repr__(self):
        return self.__str__()

start = Node()
grid[y_offset][x_offset] = start

previous = start
for i in range(len(commands)):
    command = commands[i]
    for _ in range(command[1]):
        if command[0] == "U":
            y += 1
            if grid[y_offset+y][x_offset+x] is None:
                grid[y_offset+y][x_offset+x] = Node(down=previous)
            else:
                grid[y_offset+y][x_offset+x].down = previous
            previous.up = grid[y_offset+y][x_offset+x]
        elif command[0] == "R":
            x += 1
            if grid[y_offset+y][x_offset+x] is None:
                grid[y_offset+y][x_offset+x] = Node(left=previous)
            else:
                grid[y_offset+y][x_offset+x].left = previous
            previous.right = grid[y_offset+y][x_offset+x]
        elif command[0] == "D":
            y -= 1
            if grid[y_offset+y][x_offset+x] is None:
                grid[y_offset+y][x_offset+x] = Node(up=previous)
            else:
                grid[y_offset+y][x_offset+x].up = previous
            previous.down = grid[y_offset+y][x_offset+x]
        elif command[0] == "L":
            x -= 1
            if grid[y_offset+y][x_offset+x] is None:
                grid[y_offset+y][x_offset+x] = Node(right=previous)
            else:
                grid[y_offset+y][x_offset+x].right = previous
            previous.left = grid[y_offset+y][x_offset+x]
        else:
            raise Exception(f"Unknown command: {command[0]}")
        previous = grid[y_offset+y][x_offset+x]

total = 0
for row in reversed(grid):
    outside = False
    left = None
    for node in row:
        if node is None:
            if outside:
                total += 1
        else:
            total += 1
            if node.up is not None and node.down is not None:
                outside = not outside
            elif node.right is not None and (node.up is not None or node.down is not None):
                left = node
            elif node.left is not None and ((left.up is not None and node.down is not None) or (left.down is not None and node.up is not None)):
                outside = not outside
                left = None

print("Total:", total)
