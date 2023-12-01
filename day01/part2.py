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
    i = 0
    while i < len(line):
        is_digit = False
        if line[i].isdigit():
            char = line[i]
            is_digit = True
        elif line[i:i+3] == "one":
            char = "1"
            is_digit = True
        elif line[i:i+3] == "two":
            char = "2"
            is_digit = True
        elif line[i:i+5] == "three":
            char = "3"
            is_digit = True
        elif line[i:i+4] == "four":
            char = "4"
            is_digit = True
        elif line[i:i+4] == "five":
            char = "5"
            is_digit = True
        elif line[i:i+3] == "six":
            char = "6"
            is_digit = True
        elif line[i:i+5] == "seven":
            char = "7"
            is_digit = True
        elif line[i:i+5] == "eight":
            char = "8"
            is_digit = True
        elif line[i:i+4] == "nine":
            char = "9"
            is_digit = True
        if is_digit:
            if first is None:
                first = char
            last = char
        i += 1
    total += int(first + last)

print("Total:", total)
