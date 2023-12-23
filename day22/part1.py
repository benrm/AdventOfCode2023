#!/usr/bin/env python3

import argparse
import re
import sys

parser = argparse.ArgumentParser()
parser.add_argument("--input", "-i", default=sys.stdin, type=argparse.FileType("r"))
args = parser.parse_args()

class Point:
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

    def __str__(self):
        return f"Point(x={self.x},y={self.y},z={self.z})"

class Brick:
    def __init__(self, _id, lower, higher):
        self.id = _id
        self.lower = lower
        self.higher = higher
        self.supports = set()
        self.supported_by = set()

    def __str__(self):
        return f"Brick(id={self.id},lower={self.lower},higher={self.higher},supports={self.supports},supported by={self.supported_by})"

brick_re = re.compile("(\d+),(\d+),(\d+)~(\d+),(\d+),(\d+)")

_id = 0
bricks = {}
falling = []
for line in args.input.readlines():
    matches = brick_re.match(line)
    if not matches:
        raise Exception(f"Non-matching line: {line}")
    brick = Brick(_id, Point(int(matches[1]), int(matches[2]), int(matches[3])), Point(int(matches[4]), int(matches[5]), int(matches[6])))
    falling.append(brick)
    bricks[brick.id] = brick
    _id += 1

falling = sorted(falling, key=lambda x : x.lower.z)

maxima = {}
while len(falling) > 0:
    current = falling.pop(0)
    maxima_bricks = set()
    points = []
    for y in range(current.lower.y, current.higher.y+1):
        for x in range(current.lower.x, current.higher.x+1):
            points.append((x, y))
    max_z = 0
    for point in points:
        if point in maxima and maxima[point].id not in maxima_bricks:
            maxima_bricks.add(maxima[point].id)
            if max_z < maxima[point].higher.z:
                max_z = maxima[point].higher.z
    original = Brick(current.id, Point(current.lower.x, current.lower.y, current.lower.z), Point(current.higher.x, current.higher.y, current.higher.z))
    current.higher.z = current.higher.z - current.lower.z + max_z + 1
    current.lower.z = max_z + 1
    for _id in maxima_bricks:
        brick = bricks[_id]
        if brick.higher.z+1 == current.lower.z and brick.lower.x <= current.higher.x and brick.higher.x >= current.lower.x and brick.lower.y <= current.higher.y and brick.higher.y >= current.lower.y:
            brick.supports.add(current.id)
            current.supported_by.add(brick.id)
    for point in points:
        maxima[point] = current

total = 0
for brick in bricks.values():
    can_disintegrate = True
    for _id in brick.supports:
        if len(bricks[_id].supported_by) <= 1:
            can_disintegrate = False
            break
    if can_disintegrate:
        total += 1
print("Total:", total)
