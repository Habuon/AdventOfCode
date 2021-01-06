memory = dict()


def process(mask, value):
    res = list(bin(int(value))[2:])
    while len(res) < 36:
        res = ["0"] + res
    for i in range(len(mask)):
        if mask[i] == "X":
            continue
        res[i] = mask[i]
    return int("".join(res), 2)


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
        memory[position] = process(mask, value)

r = 0
for key in memory:
    r += memory[key]

print(r)
