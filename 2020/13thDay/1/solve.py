time = 0
buses = []

with open("data.txt", "r") as file:
    time = int(file.readline().strip())
    buses = [int(x) for x in file.readline().strip().split(",") if x != "x"]


def solve(time, buses):
    new_time = time
    while True:
        for bus in buses:
            if new_time % bus == 0:
                return new_time, bus
        new_time += 1


new_time, bus = solve(time, buses)

wait = new_time - time

print(bus * wait)
