#!/usr/bin/env python3

import argparse
import sys

parser = argparse.ArgumentParser()
parser.add_argument("--input", "-i", default=sys.stdin, type=argparse.FileType("r"))
args = parser.parse_args()

class History:
    def __init__(self, array, parent=None):
        self.array = array
        self.parent = parent
        all_zeroes = True
        for item in self.array:
            if item != 0:
                all_zeroes = False
                break
        differences = [ array[i] - array[i-1] for i in range(1, len(array)) ]
        if all_zeroes:
            self.child = None
        else:
            self.child = History(differences, self)

    def print(self):
        print(self.array)
        if self.child is not None:
            self.child.print()

histories = []
for line in args.input.readlines():
    histories.append(History([ int(num) for num in line.split() ]))

_sum = 0
for i in range(len(histories)):
    history = histories[i]
    while history.child is not None:
        history = history.child
    while True:
        if history.child is None:
            history.array.insert(0, 0)
        else:
            history.array.insert(0, history.array[0]-history.child.array[0])
        if history.parent is not None:
            history = history.parent
        else:
            break
    _sum += history.array[0]
print("Sum:", _sum)
