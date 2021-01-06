numbers = []


with open("data.txt", "r") as file:
    for line in file:
        line = line.strip()
        if len(line) == 0:
            continue
        numbers.append(int(line))

def sub(arr, invalid=22477624):
    n = len(arr)
    for i in range(n): 
        curr_sum = arr[i] 
        j = i + 1
        while j <= n: 
            if curr_sum == invalid:                    
                return arr[i: j]
                  
            if curr_sum > invalid or j == n: 
                break
              
            curr_sum = curr_sum + arr[j] 
            j += 1

    return []

s = sub(numbers)
min_s, max_s = min(s), max(s)
print(min_s + max_s)
