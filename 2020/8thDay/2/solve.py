program = []

with open("data.txt", "r") as file:
    for line in file:
        line = line.strip()
        if len(line) == 0:
            continue
        line = line.split(" ")
        line[1] = int(line[1])
        program.append(line)

def solve(program):
    index = 0
    indexes = set()
    accumulator = 0
    while index != len(program) - 1:
        instruction, argument = program[index]
        indexes.add(index)
        if instruction == "nop":
            index += 1
        if instruction == "acc":
            accumulator += argument
            index += 1
        if instruction == "jmp":
            index += argument
        if index in indexes:
            return False
    return accumulator
    

def bruteforce():
    p = list(program)
    for i in range(len(p)):
        instruction, argument = p[i]
        if instruction == "nop":
            p[i][0] = "jmp"
            res = solve(p)
            if res is not False:
                return res
            p[i][0] = "nop"
        if instruction == "jmp":
            p[i][0] = "nop"
            res = solve(p)
            if res is not False:
                return res
            p[i][0] = "jmp"
    
        
    
print(bruteforce())
