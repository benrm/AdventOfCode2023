#!/usr/bin/env python3

import argparse
import re
import sys

parser = argparse.ArgumentParser()
parser.add_argument("--input", "-i", default=sys.stdin, type=argparse.FileType("r"))
args = parser.parse_args()

modules = {}
pulses = []

class Module:
    def __init__(self, name, outputs=[]):
        self.name = name
        self.outputs = outputs
        self.inputs = []

    def add_input(self, _input):
        self.inputs.append(_input)

    def pulse(self, _input, value):
        pass

class FlipFlop(Module):
    def __init__(self, name, outputs):
        super().__init__(name, outputs)
        self.on = False

    def __str__(self):
        return f"FlipFlop(name={self.name};outputs={self.outputs};inputs={self.inputs};on={self.on})"

    def pulse(self, _input, value):
        if value == False:
            self.on = not self.on
            for key in self.outputs:
                pulses.append((self.name, key, self.on))

class Conjunction(Module):
    def __init__(self, name, outputs):
        super().__init__(name, outputs)
        self.inputs = {}

    def __str__(self):
        return f"Conjunction(name={self.name};outputs={self.outputs};inputs={self.inputs})"

    def add_input(self, _input):
        self.inputs[_input] = False

    def pulse(self, _input, value):
        global pulses
        self.inputs[_input] = value
        ret = False
        for key in self.inputs:
            if self.inputs[key] == False:
                ret = True
                break
        for key in self.outputs:
            pulses.append((self.name, key, ret))

class Broadcast(Module):
    def __init__(self, outputs):
        super().__init__("broadcaster", outputs)

    def __str__(self):
        return f"Broadcast(name={self.name};outputs={self.outputs};inputs={self.inputs})"

    def pulse(self, _input, value):
        global pulses
        for output in self.outputs:
            pulses.append((_input, output, value))

module_re = re.compile("([%&]?\w+)\s+->\s+([\w\s,]+)")

for line in [ line.strip() for line in args.input.readlines() ]:
    matches = module_re.match(line)
    if not matches:
        raise Exception(f"Non-matching line: {line.strip()}")
    name = matches[1]
    outputs = matches[2].split(", ")
    if name == "broadcaster":
        modules[name] = Broadcast(outputs)
    elif name[0] == "%":
        modules[name[1:]] = FlipFlop(name[1:], outputs)
    elif name[0] == "&":
        modules[name[1:]] = Conjunction(name[1:], outputs)

for module in modules:
    for output in modules[module].outputs:
        if output in modules:
            modules[output].add_input(module)

i = 0
j = 0
while i < 1000:
    pulses.append((None, "broadcaster", False))
    while j < len(pulses):
        _pulse = pulses[j]
        if _pulse[1] in modules:
            modules[_pulse[1]].pulse(_pulse[0], _pulse[2])
        j += 1
    i += 1

low = 0
high = 0
for _pulse in pulses:
    if _pulse[2]:
        high += 1
    else:
        low += 1

print("Result:", high * low)
