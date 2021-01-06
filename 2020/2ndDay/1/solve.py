count = 0

with open("data.txt", "r") as file:
    for line in file:
        policy, password = line.strip().split(":")
        num_range, character = policy.split(" ")
        minimum, maximum = [int(x) for x in num_range.split("-")]
        if(minimum <= password.count(character) <= maximum):
            count += 1

print(count)
