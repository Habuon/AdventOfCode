result = 0
passport = ""

def is_valid(pasport):
    fields = passport.split(" ")
    fields = [x.split(":")[0] for x in fields if len(x) > 0]
    for attribute in ["byr", "iyr", "eyr", "hgt", "hcl", "ecl", "pid"]:
        if attribute not in fields:
            print(fields, attribute)
            return False
    return True

with open("data.txt", "r") as file:
    for line in file:
        if len(line.strip()) == 0:
            if is_valid(passport):
                result += 1
            passport = ""                
            continue
        passport += " " + line.strip()

print(result)
