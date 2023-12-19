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

    def exec(self, x):
        if self.op == "<":
            return x[self.element] < self.num
        elif self.op == ">":
            return x[self.element] > self.num
        else:
            raise Exception(f"Unknown op: {self.op}")

    def __str__(self):
        return f"Test(x{self.op}{self.num})"

    def __repr__(self):
        return self.__str__()

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

part_re = re.compile("{(.*)}")
rating_re = re.compile("([xmas])=(\d+)")

parts = []
while i < len(lines):
    matches = part_re.match(lines[i])
    if not matches:
        raise Exception(f"Line doesn't match part regex: {lines[i]}")
    part = {}
    words = matches[1].split(",")
    for word in words:
        matches = rating_re.match(word)
        if not matches:
            raise Exception(f"Word doesn't match rating regex: {word}")
        part[matches[1]] = int(matches[2])
    parts.append(part)

    i += 1

for part in parts:
    tests = workflows["in"].copy()
    finished = False
    while len(tests) > 0 and not finished:
        test = tests.pop(0)
        if test[0] is None or test[0].exec(part):
            if test[1] == "A":
                accepted.append(part)
                finished = True
            elif test[1] == "R":
                rejected.append(part)
                finished = True
            else:
                tests = workflows[test[1]].copy()

total = 0
for part in accepted:
    for element in part:
        total += part[element]
print("Total:", total)
