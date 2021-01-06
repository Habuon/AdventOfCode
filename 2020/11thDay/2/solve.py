seats = []

with open("data.txt", "r") as file:
    for line in file:
        line = line.strip()
        if len(line) == 0:
            continue
        seats.append(list(line))

def check_is(seats, row, col, rd, cd):
    try:
        while True:
            if row < 0 or col < 0:
                break
            if seats[row][col] == "#":
                return True
            if seats[row][col] == "L":
                return False
            row += rd
            col += cd
        return False
    except:
        return False


def number_attached(seats, row, col):
    result = 0
    for r in [-1, 0, 1]:
        for c in [-1, 0, 1]:
            if c == 0 and r == 0:
                continue
            if check_is(seats, row + r, col + c, r, c):
                result += 1    
    return result

def one_round(s):
    seats = copy(s)       
    
    for row in range(len(seats)):
        for col in range(len(seats[row])):
            if s[row][col] == "L":
                if number_attached(s, row, col) == 0:
                    seats[row][col] = "#"
            elif s[row][col] == "#":
                if number_attached(s, row, col) >= 5:
                    seats[row][col] = "L"
    
    return seats

def copy(arr):
    res = list(arr)
    for i in range(len(arr)):
        res[i] = list(arr[i])
    return res

def equal(arr1, arr2):
    for i in range(len(arr1)):
        for j in range(len(arr1[i])):
            if arr1[i][j] != arr2[i][j]:
                return False
    return True

def represent(array):
    print("\n".join([" ".join(x) for x in array]))

def count(array):
    r = 0
    for i in range(len(array)):
        for j in range(len(array[i])):
            if array[i][j] == "#":
                r += 1
    return r
    

new = one_round(seats)
while True:
    n = copy(new)
    new = one_round(new)
    if equal(n, new):
        break

print(count(new))
