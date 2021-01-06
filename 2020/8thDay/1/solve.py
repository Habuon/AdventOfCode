program = []

with open("data.txt", "r") as file:
    for line in file:
        line = line.strip()
        if len(line) == 0:
            continue
        line = line.split(" ")
        line[1] = int(line[1])
        program.append(line)

index = 0
indexes = set()
accumulator = 0
while index not in indexes:
    instruction, argument = program[index]
    indexes.add(index)
    if instruction == "nop":
        index += 1
    if instruction == "acc":
        accumulator += argument
        index += 1
    if instruction == "jmp":
        index += argument
        
    
print(accumulator)
