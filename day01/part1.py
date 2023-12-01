#!/usr/bin/env python3

import argparse
import sys

parser = argparse.ArgumentParser()
parser.add_argument("--input", "-i", default=sys.stdin, type=argparse.FileType("r"))
args = parser.parse_args()

total = 0
for line in args.input.readlines():
    first = None
    last = None
    for char in line:
        if char.isdigit():
            if first is None:
                first = char
            last = char
    total += int(first + last)

print("Total:", total)
