seats = []

with open("data.txt", "r") as file:
    for line in file:
        line = line.strip()
        if len(line) == 0:
            continue
        seats.append(list(line))


def number_attached(seats, row, col):
    result = 0
    for r in [-1, 0, 1]:
        rr = row + r
        if rr < 0:
            continue
        for c in [-1, 0, 1]:
            cc = col + c
            if cc < 0:
                continue
            if rr == row and cc == col:
                continue
            try:
                if seats[rr][cc] == "#":
                    result += 1
            except:
                pass
    return result

def one_round(s):
    seats = copy(s)       
    
    for row in range(len(seats)):
        for col in range(len(seats[row])):
            if s[row][col] == "L":
                if number_attached(s, row, col) == 0:
                    seats[row][col] = "#"
            elif s[row][col] == "#":
                if number_attached(s, row, col) >= 4:
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
while not equal(one_round(new), new):
    new = one_round(new)

print(count(new))
