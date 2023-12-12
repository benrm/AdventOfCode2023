#!/usr/bin/env python3

import argparse
import re
import sys

parser = argparse.ArgumentParser()
parser.add_argument("--input", "-i", default=sys.stdin, type=argparse.FileType("r"))
args = parser.parse_args()

lines = args.input.readlines()

map_name_re = re.compile("([\w-]+) map:")
seeds_re = re.compile("seeds:\s+([\d\s]+)")
seed_re = re.compile("\d+")

class Range:
    def __init__(self, origin, length):
        self.origin = origin
        self.length = length

    def __eq__(self, other):
        return self.origin == other.origin and self.length == other.length

    def __str__(self):
        return f"Range(origin={self.origin};range={self.length})"

    def __repr__(self):
        return self.__str__()

    def copy(self):
        return Range(self.origin, self.length)

class RangeMap:
    def __init__(self, dst, src, length):
        self.dst = Range(dst, length)
        self.src = Range(src, length)

    def __str__(self):
        return f"RangeMap(dst={self.dst},src={self.src})"

    def __repr__(self):
        return self.__str__()

def map_to(_range_maps, _id):
    for _range in _range_maps:
        if _range.src.origin <= _id and _id < _range.src.origin+_range.src.length:
            return _id - _range.src.origin + _range.dst.origin
    return _id

matches = seeds_re.match(lines[0])
if not matches:
    raise Exception(f"Line did not match seeds format: {lines[0]}")
seeds = { int(_seed) for _seed in seed_re.findall(matches[1]) }

resource_to = {}
i = 2
while i < len(lines):
    while i < len(lines):
        if lines[i].strip():
            break
        i += 1

    matches = map_name_re.match(lines[i])
    if not matches:
        raise Exception(f"Line did not match map format: {lines[i]}")
    name = matches[1]
    i += 1

    maps = []
    while i < len(lines):
        if not lines[i].strip():
            break
        maps.append(RangeMap(*[ int(word) for word in lines[i].split() ]))
        i += 1
    resource_to[name] = maps

lowest_location = None
for _seed in seeds:
    soil = map_to(resource_to["seed-to-soil"], _seed)
    fertilizer = map_to(resource_to["soil-to-fertilizer"], soil)
    water = map_to(resource_to["fertilizer-to-water"], fertilizer)
    light = map_to(resource_to["water-to-light"], water)
    temperature = map_to(resource_to["light-to-temperature"], light)
    humidity = map_to(resource_to["temperature-to-humidity"], temperature)
    location = map_to(resource_to["humidity-to-location"], humidity)
    if lowest_location is None or location < lowest_location:
        lowest_location = location
print("Location:", lowest_location)
