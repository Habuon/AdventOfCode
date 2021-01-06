instructions = []

with open("data.txt", "r") as file:
    for line in file:
        line = line.strip()
        if len(line) == 0:
            continue
        line = list(line)
        instructions.append([line[0], int("".join(line[1:]))])

class Direction:
    def __init__(self, name):
        self.name = name
        self.right = None
        self.left = None
        self.distance = 0


E = Direction("E")
N = Direction("N")
S = Direction("S")
W = Direction("W")
E.left = N
E.right = S
N.left = W
N.right = E
W.left = S
W.right = N
S.left = E
S.right = W
directions = {"E": E, "W": W, "S": S, "N": N}

heading = E

for instruction in instructions:
    move, amount = instruction
    if move in directions:
        directions[move].distance += amount
    elif move == "F":
        heading.distance += amount
    else:
        amount = amount // 90
        for i in range(amount):
            if move == "R":
                heading = heading.right
            else:
                heading = heading.left

ns = abs(N.distance - S.distance)
we = abs(W.distance - E.distance)
print(ns + we)


            
    

