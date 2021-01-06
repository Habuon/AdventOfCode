numbers = []


with open("data.txt", "r") as file:
    for line in file:
        line = line.strip()
        if len(line) == 0:
            continue
        numbers.append(int(line))

def check(index):
    for i in range(index - 25, index):
        for j in range(i + 1, index):
            if numbers[i] + numbers[j] == numbers[index]:
                return True
    return False


for i in range(25, len(numbers)):
    if not check(i):
        print(numbers[i])
        break
