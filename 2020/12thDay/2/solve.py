instructions = []

with open("data.txt", "r") as file:
    for line in file:
        line = line.strip()
        if len(line) == 0:
            continue
        line = list(line)
        instructions.append([line[0], int("".join(line[1:]))])



class Directions:
    class Direction:
        def __init__(self, name):
            self.name = name
            self.right = None
            self.left = None
            self.distance = 0

        def __repr__(self):
            return f"{self.name}: {self.distance}"
        
    def __init__(self):
        E = self.Direction("E")
        N = self.Direction("N")
        S = self.Direction("S")
        W = self.Direction("W")
        E.left = N
        E.right = S
        N.left = W
        N.right = E
        W.left = S
        W.right = N
        S.left = E
        S.right = W
        self.directions = {"E": E, "W": W, "S": S, "N": N}

    def __getitem__(self, key):
        return self.directions[key]

    def __setitem__(self, key, value):
        self.directions[key] = value

    def __iter__(self):
        yield from self.directions

    def __repr__(self):
        return repr(self.directions)

    
    def ns(self):
        return abs(self.directions["N"].distance
                   - self.directions["S"].distance)
    def we(self):
        return abs(self.directions["W"].distance
                   - self.directions["E"].distance)
        

class Waypoint:
    def __init__(self):
        self.directions = Directions()
        self.directions["N"].distance = 1
        self.directions["E"].distance = 10
        self.position = [self.directions["E"], self.directions["N"]]
        
    def rotate(self, where):
        distances = {self.directions[x] : self.directions[x].distance for x in self.directions}
        if where == "L":
            self.position = [x.left for x in self.position]
            for key in self.directions:
                self.directions[key].distance = distances[self.directions[key].right]
        else:
            self.position = [x.right for x in self.position]
            for key in self.directions:
                self.directions[key].distance = distances[self.directions[key].left]
                

    def move(self, where, amount):
        self.directions[where].distance += amount

    def ns(self):
        return abs(self.directions["N"].distance - self.directions["S"].distance)
    def we(self):
        return abs(self.directions["W"].distance - self.directions["E"].distance)

    def heading(self):
        res = [None, None]
        for key in self.directions:
            if self.directions[key] == self.position[0]:
                res[0] = key
            if self.directions[key] == self.position[1]:
                res[1] = key
        return res

    def getDistance(self, name):
        return self.directions[name].distance 
            
                




directions = Directions()
m = Waypoint()


for instruction in instructions:
    move, amount = instruction
    print(move, amount, end=" | ")
    if move in directions:
        m.move(move, amount)
        print("waypoint:", m.directions)
    elif move == "F":
        for i in range(amount):
            for key in directions:
                directions[key].distance += m.getDistance(key)
        
        print("ship:", directions, m.heading())
    else:
        amount = amount // 90
        for i in range(amount):
            m.rotate(move)
        
        print("rotate:", m.directions)

ns = abs(directions["N"].distance - directions["S"].distance)
we = abs(directions["W"].distance - directions["E"].distance)
print(ns + we)


            
    

