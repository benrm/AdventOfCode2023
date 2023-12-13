#!/usr/bin/env python3

import argparse
import re
import sys

parser = argparse.ArgumentParser()
parser.add_argument("--input", "-i", default=sys.stdin, type=argparse.FileType("r"))
args = parser.parse_args()

entry_re = re.compile("([#\.?]+)\s+([\d,]+)")

lines = []
for line in args.input.readlines():
    matches = entry_re.match(line)
    if not matches:
        raise Exception(f"Non-matching line: {line}")
    lines.append((matches[1], [ int(i) for i in matches[2].split(",") ]))

def gen_check(array):
    check = []
    count = 0
    for char in array:
        if char == "#":
            count += 1
        elif count > 0:
            check.append(count)
            count = 0
    if count > 0:
        check.append(count)
    return check

def compare_partial_check(partial, actual):
    if len(partial) == 0:
        return True
    if len(partial) > len(actual):
        return False
    for i in range(len(partial)-1):
        if partial[i] != actual[i]:
            return False
    return partial[len(partial)-1] <= actual[len(partial)-1]

def compare_check(generated, actual):
    if len(generated) != len(actual):
        return False
    for i in range(len(generated)):
        if generated[i] != actual[i]:
            return False
    return True

total = 0
for line in lines:
    array, check = line
    possibilities = []
    if array[0] == "#" or array[0] == ".":
        possibilities.append([array[0]])
    else:
        possibilities.append(["#"])
        possibilities.append(["."])
    for i in range(1, len(array)):
        if array[i] == "#" or array[i] == ".":
            for possibility in possibilities:
                possibility.append(array[i])
        else:
            _next = []
            for possibility in possibilities:
                _new = possibility.copy()
                _new.append("#")
                if compare_partial_check(gen_check(_new), check):
                    _next.append(_new)
                _new = possibility.copy()
                _new.append(".")
                if compare_partial_check(gen_check(_new), check):
                    _next.append(_new)
            possibilities = _next
    for possibility in possibilities:
        if compare_check(gen_check(possibility), check):
            total += 1
print("Total:", total)
