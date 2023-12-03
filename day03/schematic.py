class Cell:
    def __init__(self, value, length=1):
        self.value = value
        self.length = length
        self.adjacent = False
        self.neighbors = []

    def __str__(self):
        if self.IsNumber():
            return f"[{self.value}, {self.adjacent}]"
        elif self.IsSymbol():
            return f"[{self.value}, {len(self.neighbors)}]"
        else:
            return f"'{self.value}'"

    def __repr__(self):
        return self.__str__()

    def IsNumber(self):
        return isinstance(self.value, int)

    def IsEmpty(self):
        return self.value == "."

    def IsSymbol(self):
        return not self.IsNumber() and not self.IsEmpty()

    def IsGear(self):
        return self.value == "*" and len(self.neighbors) == 2

    def GearRatio(self):
        if not self.IsGear():
            raise Exception("not a gear")
        product = 1
        for neighbor in self.neighbors:
            product *= neighbor.value
        return product

class Schematic:
    def __init__(self, grid, width, height):
        self.grid = grid
        self.width = width
        self.height = height

    def Print(self):
        for row in self.grid:
            print(row)

    def PrintGrid(self):
        for row in self.grid:
            for cell in row:
                print(cell.value, end="")
            print("")

    def Get(self, x, y):
        pos = 0
        for cell in self.grid[y]:
            if pos <= x and x < pos+cell.length:
                return cell
            pos += cell.length
        raise IndexError()

def LoadSchematic(lines):
    grid = []
    y = 0
    width = len(lines[0])-1
    height = len(lines)
    while y < len(lines):
        row = []
        x = 0
        while x < len(lines[y]):
            if lines[y][x] == "\n":
                break
            elif lines[y][x].isdigit():
                num = ""
                while lines[y][x].isdigit():
                    num += lines[y][x]
                    x += 1
                row.append(Cell(int(num), length=len(num)))
            else:
                row.append(Cell(lines[y][x]))
                x += 1
        grid.append(row)
        y += 1
    schematic = Schematic(grid, width, height)
    for y in range(schematic.height):
        for x in range(schematic.width):
            cell = schematic.Get(x, y)
            if cell.IsSymbol():
                min_x = x-1 if x > 0 else 0
                min_y = y-1 if y > 0 else 0
                max_x = x+1 if x+1 < schematic.width else schematic.width-1
                max_y = y+1 if y+1 < schematic.height else schematic.height-1
                neighbors = []
                for j in range(min_y, max_y+1):
                    for i in range(min_x, max_x+1):
                        if (x, y) != (i, j):
                            cell = schematic.Get(i, j)
                            if cell.IsNumber():
                                exists = False
                                for neighbor in neighbors:
                                    if neighbor == cell:
                                        exists = True
                                        break
                                if not exists:
                                    cell.adjacent = True
                                    neighbors.append(cell)
                cell = schematic.Get(x, y)
                cell.neighbors = neighbors
    return schematic
