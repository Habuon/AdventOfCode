count = 0

with open("data.txt", "r") as file:
    for line in file:
        policy, password = line.strip().split(":")
        num_range, character = policy.split(" ")
        index1, index2 = [int(x) for x in num_range.split("-")]
        if password[index1] == password[index2]:
            continue
        if(password[index1] == character):
            count += 1
        if(password[index2] == character):
            count += 1

print(count)
