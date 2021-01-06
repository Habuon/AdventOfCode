
result = 0
groups = []
group = []
with open("data.txt", "r") as file:
    for line in file:
        if len(line.strip()) == 0:
            groups.append(group)
            group = []
            continue
        person = set()
        for quiestion in list(line.strip()):
            person.add(quiestion)
        group.append(person)

for i in range(len(groups)):
    p = groups[i][0]
    for person in groups[i]:
        p = p.intersection(person)
    groups[i] = p

r = 0

for group in groups:
    r += len(group)

print(r)
        
