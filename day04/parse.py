
import re

line_re = re.compile("Card\s+(\d+):\s+([\d\s]+)\s+\|\s+([\d\s]+)")

def ParseLines(lines):
    cards = []
    for line in lines:
        matches = line_re.search(line)
        if not matches:
            raise Exception(f"Non-matching line: {line}")
        cards.append({
            "id": int(matches[1]),
            "winners": { int(num) for num in matches[2].split() },
            "contents": [ int(num) for num in matches[3].split() ]
        })
    return cards
