adapters = []

with open("data.txt", "r") as file:
    for line in file:
        line = line.strip()
        if len(line) == 0:
            continue
        adapters.append(int(line))

adapters = sorted(adapters)

differences = dict()

for i in range(1, len(adapters)):
    diff = adapters[i] - adapters[i - 1]
    if diff not in differences:
        differences[diff] = 0
    differences[diff] += 1
    
differences[1] += 1
differences[3] += 1

print(differences[1] * differences[3])
