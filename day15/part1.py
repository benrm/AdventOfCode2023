#!/usr/bin/env python3

import argparse
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

total = 0
for entry in entries:
    total += hash(entry)
print("Total:", total)
