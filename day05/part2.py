#!/usr/bin/env python3

import argparse
import re
import seed
import sys

parser = argparse.ArgumentParser()
parser.add_argument("--input", "-i", default=sys.stdin, type=argparse.FileType("r"))
args = parser.parse_args()

lines = args.input.readlines()

seeds_re = re.compile("seeds:\s+([\d\s]+)")
seed_re = re.compile("\d+")

matches = seeds_re.match(lines[0])
if not matches:
    raise Exception(f"Line did not match seeds format: {lines[0]}")
matches = seed_re.findall(matches[1])
ranges = []
for i in range(0,len(matches),2):
    ranges.append(seed.Range(int(matches[i]), int(matches[i+1])))

maps = seed.parse(lines[2:])

soils = seed.map_range_to(maps["seed-to-soil"], ranges)
fertilizers = seed.map_range_to(maps["soil-to-fertilizer"], soils)
waters = seed.map_range_to(maps["fertilizer-to-water"], fertilizers)
lights = seed.map_range_to(maps["water-to-light"], waters)
temperatures = seed.map_range_to(maps["light-to-temperature"], lights)
humiditys = seed.map_range_to(maps["temperature-to-humidity"], temperatures)
locations = seed.map_range_to(maps["humidity-to-location"], humiditys)
lowest_location = None
for location in locations:
    if lowest_location is None or location.origin < lowest_location:
        lowest_location = location.origin
print("Location:", lowest_location)
