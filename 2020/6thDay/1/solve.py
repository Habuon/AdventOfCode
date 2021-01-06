
result = 0
groups = []
group = set()

with open("data.txt", "r") as file:
    for line in file:
        if len(line.strip()) == 0:
            groups.append(group)
            group = set()
            continue
        for quiestion in list(line.strip()):
            group.add(quiestion)
            result += 1

r = 0

for group in groups:
    r += len(group)

print(r)
        
