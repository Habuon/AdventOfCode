result = 0
passport = ""

class Valildator:
    def __init__(self):
        self.dictionary = {"byr": self.byr, "iyr": self.iyr,
                           "eyr": self.eyr, "hgt": self.hgt,
                           "hcl": self.hcl, "ecl": self.ecl,
                           "pid": self.pid}

    def validate(self, field, value):
        return self.dictionary[field](value)

    def number(self, value, minimum, maximum):
        try:
            year = int(value)
        except:
            return False
        if year < minimum or year > maximum:
            return False
        return True

    def byr(self, value):
        return self.number(value, 1920, 2002)

    def iyr(self, value):
        return self.number(value, 2010, 2020)

    def eyr(self, value):
        return self.number(value, 2020, 2030)

    def hgt(self, value):
        try:
            part = value[-2:]
        except:
            return False
        if part == "cm":
            return self.number(value[:-2], 150, 193)
        if part == "in":
            return self.number(value[:-2], 59, 76)
        return False

    def hcl(self, value):
        if value[0] != "#":
            return False
        value = value[1:]
        if len(value) != 6:
            return False
        try:
            num = int(value, 16)
            return True
        except:
            return False

    def ecl(self, value):
        return value in ["amb", "blu", "brn", "gry", "grn", "hzl", "oth"]

    def pid(self, value):
        if len(value) != 9:
            return False
        try:
            num = int(value)
            return True
        except:
            return False
    
validator = Valildator()

def is_valid(pasport):
    fields = passport.split(" ")
    fields = {x.split(":")[0]:x.split(":")[1]  for x in fields if len(x) > 0}
    for attribute in ["byr", "iyr", "eyr", "hgt", "hcl", "ecl", "pid"]:
        if attribute not in fields:
            return False
        if validator.validate(attribute, fields[attribute]) is False:
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
