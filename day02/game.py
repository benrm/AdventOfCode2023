import re

line_re = re.compile("Game (\d+): (.*)")
blue_re = re.compile("(\d+) blue")
red_re = re.compile("(\d+) red")
green_re = re.compile("(\d+) green")

class Round:
    def __init__(self, blue, red, green):
        self.blue = blue
        self.red = red
        self.green = green
    
    def Print(self):
        print("Round: blue %d, red %d, green %d" % (self.blue, self.red, self.green))

    def Possible(self, red, blue, green):
        return self.red <= red and self.blue <= blue and self.green <= green

class Game:
    def __init__(self, id, rounds):
        self.id = id
        self.rounds = rounds

    def Print(self):
        print("Game %d:" % self.id)
        for round in self.rounds:
            round.Print()

    def Possible(self, red, blue, green):
        for round in self.rounds:
            if not round.Possible(red, blue, green):
                return False
        return True

    def MinimumProduct(self):
        blue, red, green = 0, 0, 0
        for round in self.rounds:
            if blue < round.blue:
                blue = round.blue
            if red < round.red:
                red = round.red
            if green < round.green:
                green = round.green
        return blue * red * green

def ParseGames(line):
    matches = line_re.match(line)
    if not matches:
        raise Exception("Line in unexpected format: %s" % line)
    id = int(matches[1])
    round_strs = re.split(";", matches[2])
    rounds = []
    for round_str in round_strs:
        matches = blue_re.search(round_str)
        blue = int(matches[1]) if matches else 0
        matches = red_re.search(round_str)
        red = int(matches[1]) if matches else 0
        matches = green_re.search(round_str)
        green = int(matches[1]) if matches else 0
        rounds.append(Round(blue, red, green))
    return Game(id, rounds)
