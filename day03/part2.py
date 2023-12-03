#!/usr/bin/env python3

import argparse
from schematic import LoadSchematic
import sys

parser = argparse.ArgumentParser()
parser.add_argument("--input", "-i", default=sys.stdin, type=argparse.FileType("r"))
args = parser.parse_args()

schematic = LoadSchematic(args.input.readlines())

total = 0
for row in schematic.grid:
    for cell in row:
        if cell.IsGear():
            total += cell.GearRatio()
print("Total:", total)
