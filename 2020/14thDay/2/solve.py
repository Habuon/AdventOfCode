memory = dict()


def process(mask, value):
    res = list(bin(int(value))[2:])
    while len(res) < 36:
        res = ["0"] + res
    for i in range(len(mask)):
        if mask[i] == "0":
            continue
        res[i] = mask[i]
    return [int(x, 2) for x in all_possible("".join(res))]

def all_possible(value):
    if value.count("X") == 0:
        return [value]
    result = []
    result += all_possible(value[: value.find("X")] + "0" + value[value.find("X") + 1:])
    result += all_possible(value[: value.find("X")] + "1" + value[value.find("X") + 1:])
    return result
            
        

with open("data.txt", "r") as file:
    for line in file:
        line = line.strip()
        if len(line) == 0:
            continue
        command, value = line.replace(" ", "").split("=")
        if command == "mask":
            mask = value
            continue

        position = int(command.split("[")[1].split("]")[0])
        positions = process(mask, position)
        for position in positions:
            memory[position] = int(value)


r = 0
for key in memory:
    r += memory[key]
