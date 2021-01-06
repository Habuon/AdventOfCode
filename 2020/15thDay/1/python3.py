def merge_sort(pole):
    def merge(a, b, c):
        # prvý úsek range(a, b), druhý úsek range(b, c)
        i, j = a, b
        while i + j < c - a:
            if j == c - b or i < b - a and pole[i] < pole[j]:
                pole[i+j] = pole[i]
                i += 1
            else:
                pole[i+j] = pole[j]
                j += 1

    n = len(pole)
    k = 1
    while k < n:
        i = 0
        while i + k < n:
            merge(i, i+k, min(i+2*k, n))
            i += 2*k
        k += k

pole = [108, 162, 670, 866, 533, 589, 450, 328, 154, 812, 875, 912, 955,
        493, 894, 534, 389, 439, 798, 770, 603, 131, 190, 699, 109, 385,
        430, 693, 367, 605, 547, 551, 364, 937, 492, 438, 499, 448, 719,
        759, 213, 962, 938, 437, 365, 364, 984, 636, 467, 465, 961, 875,
        442, 817, 594, 568, 180, 484, 475, 608, 207, 417, 706, 470, 468,
        145, 351, 824, 836, 520, 740, 987, 187, 453, 822, 262, 700, 779,
        535, 672, 184, 132, 853, 568, 904, 859, 820, 159, 307, 175, 198,
        174, 446, 640, 762, 522, 356, 470, 655, 377, 796, 517, 298, 293,
        865, 821, 537, 928, 609, 994, 537]

# merge_sort(pole)

def six():
    slova = set()
    five = set()
    with open("subor.txt", "r") as file:
        for line in file:
            line = line.strip()
            if len(line) == 0:
                continue
            for slovo in line.split(" "):
                if len(slovo) == 5:
                    five.add(slovo)
                slova.add(slovo)

    print(len(five), len(slova))
