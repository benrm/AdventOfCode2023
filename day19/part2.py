#!/usr/bin/env python3

import argparse
import re
import sys

parser = argparse.ArgumentParser()
parser.add_argument("--input", "-i", default=sys.stdin, type=argparse.FileType("r"))
args = parser.parse_args()

lines = args.input.readlines()

workflows = {}
accepted = []
rejected = []

name_re = re.compile("(\w+){")
body_re = re.compile("\w+{(.*)}")
test_re = re.compile("(\w+)([<>])(\d+):(\w+)")

class Test:
    def __init__(self, element, op, num):
        self.element = element
        self.op = op
        self.num = num

    def __str__(self):
        return f"Test({self.element}{self.op}{self.num})"

    def __repr__(self):
        return self.__str__()

    def split(self, part_range):
        if self.op == "<":
            if part_range[self.element][1] < self.num:
                return (part_range.copy(), None)
            elif part_range[self.element][0] < self.num and self.num <= part_range[self.element][1]:
                truthy = part_range.copy()
                truthy[self.element] = (part_range[self.element][0], self.num-1)
                falsy = part_range.copy()
                falsy[self.element] = (self.num, part_range[self.element][1])
                return (truthy, falsy)
            elif self.num <= part_range[self.element][0]:
                return (None, part_range.copy())
            else:
                raise Exception(f"Unhandled range: {self} {part_range}")
        elif self.op == ">":
            if part_range[self.element][1] <= self.num:
                return (None, part_range.copy())
            elif part_range[self.element][0] <= self.num and self.num < part_range[self.element][1]:
                truthy = part_range.copy()
                truthy[self.element] = (self.num+1, part_range[self.element][1])
                falsy = part_range.copy()
                falsy[self.element] = (part_range[self.element][0], self.num)
                return (truthy, falsy)
            elif self.num < part_range[self.element][0]:
                return (part_range.copy(), None)
            else:
                raise Exception(f"Unhandled range: {self} {part_range}")
        else:
            raise Exception(f"Unhandled op: {self.op}")

i = 0
while i < len(lines):
    if len(lines[i].strip()) == 0:
        i += 1
        break

    matches = name_re.match(lines[i])
    if not matches:
        raise Exception(f"Line doesn't match name regex: {lines[i]}")
    name = matches[1]

    matches = body_re.search(lines[i])
    if not matches:
        raise Exception(f"Line doesn't match body regex: {lines[i]}")
    body = matches[1]

    test_strs = body.split(",")
    tests = []
    for test_str in test_strs:
        matches = test_re.match(test_str)
        if matches:
            element = matches[1]
            op = matches[2]
            num = int(matches[3])
            target = matches[4]
            tests.append((Test(element, op, num), target))
        else:
            tests.append((None, test_str))

    workflows[name] = tests

    i += 1

working = [ ({ "x": (1, 4000), "m": (1, 4000), "a": (1, 4000), "s": (1, 4000) }, "in") ]

while len(working) > 0:
    current = working.pop(0)
    tests = workflows[current[1]].copy()
    finished = False
    while len(tests) > 0 and not finished:
        test = tests.pop(0)
        if test[0] is None:
            if test[1] == "A":
                accepted.append(current[0])
            elif test[1] == "R":
                rejected.append(current[0])
            else:
                working.append((current[0], test[1]))
        else:
            (truthy, falsy) = test[0].split(current[0])
            if truthy is not None:
                if test[1] == "A":
                    accepted.append(truthy)
                elif test[1] == "R":
                    rejected.append(truthy)
                else:
                    working.append((truthy, test[1]))
            if falsy is not None:
                current = (falsy, current[1])
            else:
                finished = True

def get_range(_range):
    return _range[1] - _range[0] + 1

total = 0
for part_range in accepted:
    total += get_range(part_range["x"]) * get_range(part_range["m"]) * get_range(part_range["a"]) * get_range(part_range["s"])
print("Total:", total)
