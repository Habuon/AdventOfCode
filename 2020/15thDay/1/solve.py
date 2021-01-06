numbers = []
with open("data.txt", "r") as file:
    numbers += [int(x) for x in file.readline().strip().split(",")]

while len(numbers) < 30000002:
    number = numbers[-1]
    if numbers.count(number) == 1:
        numbers.append(0)
        continue
    n = list(numbers)
    n.reverse()
    i = n.index(number)
    n = n[i + 1: ]
    j = n.index(number)
    numbers.append(j - i + 1)
    
print(numbers[30000000 - 1])
