#!/usr/bin/env python3

import argparse
from game import ParseGames
import sys

parser = argparse.ArgumentParser()
parser.add_argument("--input", "-i", default=sys.stdin, type=argparse.FileType("r"))
args = parser.parse_args()

games = []
for line in args.input.readlines():
    games.append(ParseGames(line))

total = 0
for game in games:
    total += game.MinimumProduct()
print("Total:", total)
