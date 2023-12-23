#!/usr/bin/env python3

import argparse
import sys

parser = argparse.ArgumentParser()
parser.add_argument("--input", "-i", default=sys.stdin, type=argparse.FileType("r"))
args = parser.parse_args()

class Square:
    def __init__(self, x, y, value):
        self.x = x
        self.y = y
        self.value = value
        self.steps = 0
        self.up, self.right, self.down, self.left = None, None, None, None

    def __str__(self):
        return f"Square(x={self.x},y={self.y},value={self.value},steps={self.steps})"

    def __repr__(self):
        return self.__str__()

lines = [ line.strip() for line in args.input.readlines() ]
grid = []
for y in range(len(lines)):
    row = []
    for x in range(len(lines[y])):
        row.append(Square(x, y, lines[y][x]))
    grid.append(row)

for y in range(len(grid)):
    for x in range(len(grid[y])):
        if y > 0:
            grid[y][x].up = grid[y-1][x]
        if x < len(grid[y])-1:
            grid[y][x].right = grid[y][x+1]
        if y < len(grid)-1:
            grid[y][x].down = grid[y+1][x]
        if x > 0:
            grid[y][x].left = grid[y][x-1]

class Node:
    def __init__(self, square, previous):
        self.square = square
        self.previous = previous

    def __str__(self):
        return f"Node(square={self.square})"

    def __repr__(self):
        return self.__str__()

    def visited(self, square):
        current = self
        while current.previous is not None:
            if current.previous.square.x == square.x and current.previous.square.y == square.y:
                return True
            current = current.previous
        return False

i = 0
start = None
while i < len(grid[0]) and start is None:
    if grid[0][i].value == ".":
        start = Node(grid[0][i], None)
    else:
        i += 1

end = None
while i < len(grid[len(grid)-1]) and end is None:
    if grid[len(grid)-1][i].value == ".":
        end = grid[len(grid)-1][i]
    else:
        i += 1

processing = [ start ]
while len(processing) > 0:
    current = processing.pop(0)
    square = current.square
    if (square.value == "." or square.value == "^") and square.up is not None and square.up.value != "#" and not current.visited(square.up) and square.up.steps < square.steps+1:
        processing.append(Node(square.up, current))
        square.up.steps = square.steps + 1
    if (square.value == "." or square.value == ">") and square.right is not None and square.right.value != "#" and not current.visited(square.right) and square.right.steps < square.steps+1:
        processing.append(Node(square.right, current))
        square.right.steps = square.steps + 1
    if (square.value == "." or square.value == "v") and square.down is not None and square.down.value != "#" and not current.visited(square.down) and square.down.steps < square.steps+1:
        processing.append(Node(square.down, current))
        square.down.steps = square.steps + 1
    if (square.value == "." or square.value == "<") and square.left is not None and square.left.value != "#" and not current.visited(square.left) and square.left.steps < square.steps+1:
        processing.append(Node(square.left, current))
        square.left.steps = square.steps + 1
print("Steps:", end.steps)
