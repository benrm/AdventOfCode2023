#!/usr/bin/env python3

import argparse
import re
import sys

parser = argparse.ArgumentParser()
parser.add_argument("--input", "-i", default=sys.stdin, type=argparse.FileType("r"))
args = parser.parse_args()

entries = args.input.read().strip().split(",")

def hash(string):
    current = 0
    for char in string:
        current += ord(char)
        current *= 17
        current %= 256
    return current

boxes = [ [] for i in range(256) ]

set_re = re.compile("(\w+)=(\d+)")
remove_re = re.compile("(\w+)-")

class Lens:
    def __init__(self, label, focal_length):
        self.label = label
        self.focal_length = focal_length

    def __str__(self):
        return f"Lens(label='{self.label}',focal_length={self.focal_length})"

    def __repr__(self):
        return self.__str__()

for entry in entries:
    matches = set_re.match(entry)
    if matches:
        lens = Lens(matches[1], int(matches[2]))
        idx = hash(lens.label)
        replaced = False
        for i in range(len(boxes[idx])):
            if boxes[idx][i].label == lens.label:
                boxes[idx][i] = lens
                replaced = True
                break
        if not replaced:
            boxes[idx].append(lens)
    else:
        matches = remove_re.match(entry)
        if matches:
            idx = hash(matches[1])
            for i in range(len(boxes[idx])):
                if boxes[idx][i].label == matches[1]:
                    boxes[idx].pop(i)
                    break
        else:
            raise Exception(f"Non-matching entry: {entry}")

power = 0
for i in range(len(boxes)):
    for j in range(len(boxes[i])):
        power += (i + 1) * (j + 1) * boxes[i][j].focal_length
print("Power:", power)
