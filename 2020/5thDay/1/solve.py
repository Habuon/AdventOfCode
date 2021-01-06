
arr = []
for i in range(128):
    arr.append([])
    for j in range(8):
        arr[-1].append(0)

ids = set()


def solve(array, path,r=0, c=0, row=False):
    if len(path) == 0:
        global arr
        arr[r][c] = 1
        return r, c
    if path[0] == "F":
        return solve(array[: len(array) // 2], path[1:], r=r, c=c)
    if path[0] == "B":
        return solve(array[len(array) // 2: ], path[1:], r=r + len(array) // 2, c=c)
    if path[0] == "L":
        array = array[0] if not row else array
        return solve(array[: len(array) // 2], path[1:], r=r, c=c, row=True)
    if path[0] == "R":
        array = array[0] if not row else array
        return solve(array[len(array) // 2: ], path[1:], r=r, c=c+len(array) // 2, row=True)


mx = 0

with open("data.txt", "r") as file:
    for line in file:
        r, c = solve(arr, line.strip())
        i = r * 8 + c
        ids.add(i)
        mx = max(mx, i)

print(mx)
                
