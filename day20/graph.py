#!/usr/bin/env python3

import argparse
import math
import pydot
import re
import sys

parser = argparse.ArgumentParser()
parser.add_argument("--input", "-i", default=sys.stdin, type=argparse.FileType("r"))
parser.add_argument("--output", "-o", default="graph.png")
args = parser.parse_args()

graph = pydot.Dot("Modules")

module_re = re.compile("([%&]?\w+)\s+->\s+([\w\s,]+)")

for line in [ line.strip() for line in args.input.readlines() ]:
    matches = module_re.match(line)
    if not matches:
        raise Exception(f"Non-matching line: {line.strip()}")
    name = matches[1]
    if name == "broadcaster":
        color = "red"
    elif name[0] == "%":
        name = name[1:]
        color = "green"
    elif name[0] == "&":
        name = name[1:]
        color = "blue"
    graph.add_node(pydot.Node(name, color=color))
    outputs = matches[2].split(", ")
    for output in outputs:
        graph.add_edge(pydot.Edge(name, output))

graph.write_png(args.output)
