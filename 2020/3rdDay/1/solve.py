col = 0
trees = 0

with open("data.txt", "r") as file:
    for line in file:
        line = list(line.strip())
        if line[col] == "#":
            trees += 1
        col += 3
        col = col % len(line)

print(trees)

