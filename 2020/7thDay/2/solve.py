

data = dict()
contains = dict()

with open("data.txt", "r") as file:
    for line in file:
        line = line.strip()
        if len(line) == 0:
            continue
        try:
            
            key, values = line.strip().split("contain")
            key = key.split("bag")[0].strip()
            values = values.split(",")
            values = {" ".join(x.split(" ")[2: -1]): int(x.split(" ")[1])  for x in values}   # nefunguje
            data[key] = values
        except:
            key, values = line.strip().split("contain")
            key = key.split("bag")[0].strip()
            data[key] = None


mem = dict()

def solve(key):
    global mem
    result = 0
    if key in mem:
        return mem[key]
    if data[key] is None:
        mem[key] = 0
        return 0
    for k in data[key]:
        if k in mem:
            r = data[key][k] * mem[k]
        else:
            r = data[key][k] * solve(k)
        result += r
        result += data[key][k]
    mem[key] = result
    return result
    
print(solve("shiny gold"))





        
