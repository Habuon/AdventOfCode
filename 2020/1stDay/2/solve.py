all_numbers = []
with open("data.txt", "r") as file:
    for line in file:
        all_numbers.append(int(line.strip()))

def solve(l):
    for i in range(len(all_numbers)):
        for j in range(i, len(all_numbers)):
            if all_numbers[i] + all_numbers[j] > l:
                continue
            for k in range(i, len(all_numbers)):
                if all_numbers[i] + all_numbers[j] + all_numbers[k] == l:
                    return all_numbers[i] * all_numbers[j] * all_numbers[k]


print(solve(2020))
