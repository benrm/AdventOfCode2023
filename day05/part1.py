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
seeds = { int(_seed) for _seed in seed_re.findall(matches[1]) }

maps = seed.parse(lines[2:])

lowest_location = None
for _seed in seeds:
    soil = seed.map_to(maps["seed-to-soil"], _seed)
    fertilizer = seed.map_to(maps["soil-to-fertilizer"], soil)
    water = seed.map_to(maps["fertilizer-to-water"], fertilizer)
    light = seed.map_to(maps["water-to-light"], water)
    temperature = seed.map_to(maps["light-to-temperature"], light)
    humidity = seed.map_to(maps["temperature-to-humidity"], temperature)
    location = seed.map_to(maps["humidity-to-location"], humidity)
    if lowest_location is None or location < lowest_location:
        lowest_location = location
print("Location:", lowest_location)
