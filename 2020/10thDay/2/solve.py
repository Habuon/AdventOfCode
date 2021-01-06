adapters = []

with open("data.txt", "r") as file:
    for line in file:
        line = line.strip()
        if len(line) == 0:
            continue
        adapters.append(int(line))

adapters = sorted(adapters)
p = {
    1: 1,
    2: 2,
    3: 4
    }

for i in range(3, len(adapters)):
    p[adapters[i]] = 0
    for j in range(1, 4):
        if adapters[i]  - j in  p:
            p[adapters[i]] += p[adapters[i] - j]
    
            

print(p[adapters[-1]])
