#!/usr/bin/env python3

import argparse
from parse import ParseLines
import sys

parser = argparse.ArgumentParser()
parser.add_argument("--input", "-i", default=sys.stdin, type=argparse.FileType("r"))
args = parser.parse_args()

cards = ParseLines(args.input.readlines())

total = 0
for card in cards:
    points = 0
    for content in card["contents"]:
        if content in card["winners"]:
            if points == 0:
                points = 1
            else:
                points *= 2
    total += points
print("Total:", total)
