#!/usr/bin/env python3

import argparse
import re
import sys

parser = argparse.ArgumentParser()
parser.add_argument("--input", "-i", default=sys.stdin, type=argparse.FileType("r"))
args = parser.parse_args()

line_re = re.compile("([\w\d]+) (\d+)")

_hands = [ "high_card", "one_pair", "two_pair", "three_of_a_kind", "full_house", "four_of_a_kind", "five_of_a_kind" ]
hands = { _hands[i]: i for i in range(len(_hands)) }

_cards = "23456789TJQKA"
cards = { _cards[i]: i for i in range(len(_cards)) }

class Hand:
    def __init__(self, string):
        self.string = string
        repeated = {}
        for char in self.string:
            if char in repeated:
                repeated[char] += 1
            else:
                repeated[char] = 1
        if len(repeated) == 1:
            self.type = hands["five_of_a_kind"]
        elif len(repeated) == 2:
            for char in repeated:
                if repeated[char] == 4 or repeated[char] == 1:
                    self.type = hands["four_of_a_kind"]
                else:
                    self.type = hands["full_house"]
                break
        elif len(repeated) == 3:
            for char in repeated:
                if repeated[char] == 3:
                    self.type = hands["three_of_a_kind"]
                elif repeated[char] == 2:
                    self.type = hands["two_pair"]
                else:
                    continue
                break
        elif len(repeated) == 4:
            self.type = hands["one_pair"]
        else:
            self.type = hands["high_card"]

    def __lt__(self, other):
        if self.type != other.type:
            return self.type < other.type
        for i in range(len(self.string)):
            if cards[self.string[i]] != cards[other.string[i]]:
                return cards[self.string[i]] < cards[other.string[i]]
        return False

    def __str__(self):
        return self.string

    def __repr__(self):
        return self.__str__()

wagers = []
for line in args.input.readlines():
    matches = line_re.match(line)
    if not matches:
        raise Exception(f"Non-matching line: {line}")
    wagers.append((Hand(matches[1]), int(matches[2])))

wagers = sorted(wagers)
total_winnings = 0
for i in range(len(wagers)):
    total_winnings += (i + 1) * wagers[i][1]
print("Total Winnings:", total_winnings)
