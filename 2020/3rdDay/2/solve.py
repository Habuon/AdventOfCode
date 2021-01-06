full_map = []

with open("data.txt", "r") as file:
    for line in file:
        line = list(line.strip())
        full_map.append(line)


def find(row, col):
    result = 0
    c = 0
    for i in range(0, len(full_map), row):
        line = full_map[i]
        if line[c] == "#":
            result += 1
        c += col
        c = c % len(line)
    return result


##    Right 1, down 1.
##    Right 3, down 1. 
##    Right 5, down 1.
##    Right 7, down 1.
##    Right 1, down 2.

positions = [[1, 1], [1, 3], [1, 5], [1, 7], [2, 1]]
result = 1

for position in positions:
    pom = find(position[0], position[1])
    result *= pom
    print(pom)

print()
print("result: ", result)

