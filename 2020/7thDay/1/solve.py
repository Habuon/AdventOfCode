

data = dict()
contains = dict()

with open("data.txt", "r") as file:
    for line in file:
        try:
            
            key, values = line.strip().split("contain")
            key = key.split("bag")[0].strip()
            values = values.split(",")
            values = [" ".join(x.split(" ")[2: -1])  for x in values]           
            data[key] = values
        except:
            print(line)

contains = {x : None for x in data}
for key in data:
    if "shiny gold" in data[key]:
        contains[key] = True
    if "other" in data[key]:
        contains[key] = False

def solve(key):
    global contains
    if contains[key] is not None:
        return contains[key]
    for k in data[key]:
        if solve(k):
            contains[key] = True
            return True
    
    contains[key] = False
    return False
    

not_checked = [x for x in contains if contains[x] is None]
while len(not_checked) != 0:
    key = not_checked.pop(0)
    solve(key)
    not_checked = [x for x in contains if contains[x] is None]

print(len([x for x in contains if contains[x] == True]))




        
