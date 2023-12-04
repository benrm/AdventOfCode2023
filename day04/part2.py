#!/usr/bin/env python3

import argparse
from parse import ParseLines
import sys

parser = argparse.ArgumentParser()
parser.add_argument("--input", "-i", default=sys.stdin, type=argparse.FileType("r"))
args = parser.parse_args()

cards = ParseLines(args.input.readlines())
copies = {card["id"]: 1 for card in cards }

for card in cards:
    count = 0
    for content in card["contents"]:
        if content in card["winners"]:
            count += 1
    for i in range(1,count+1):
        copies[card["id"]+i] += copies[card["id"]]
total_copies = 0
for total in copies.values():
    total_copies += total
print("Card Total:", total_copies)
