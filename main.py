import random
import string


def read_file(filename):
    """
    (str) -> (list(list))

    Read field for battleship and return list of points:
    " "(space) -> empty field
    "X" -> damaged
    "*" -> part of ship
    """
    data = []
    with open(filename) as file:
        # for line in file.readlines():
        lines = [line.rstrip() for line in file.readlines()]
        for line in lines:
            x = []
            for i in line:
                x.append(i)

            while len(x) != 10:
                x.append(" ")
            data.append(x)

    return data


# Useful functions

def index_of_letter(let):
    """
    (str) -> (int)

    Get index of letter in alphabet
    """
    letters = string.ascii_uppercase
    return letters.index(let)


def check_prop_place(data, x, y):
    """
    (data, int, int) -> (bool)

    Check if this field not border with any ships
    """

    d = [(1, 0), (1, -1), (1, 1), (0, -1), (0, 1), (-1, 0), (-1, -1), (-1, 1)]
    for delta in d:
        dx = delta[0]
        dy = delta[1]

        if 0 <= x+dx < 10 and 0 <= y+dy < 10:
            if data[x+dx][y+dy] != " ":
                return False

    return True


def check_ship_pos(data, x, y, size, horiz):
    """
    (data, int, int, int, bool) -> (bool)

    Check if you could put ship at this coordinates
    """
    if horiz:
        for i in range(y, y+size):
            if not check_prop_place(data, x, i):
                return False
        return True
    else:
        for i in range(x, x+size):
            if not check_prop_place(data, i, y):
                return False
        return True


# Basic functions

def has_ship(data, coor):
    """
    (list, tuple) -> (bool)

    Check if the ship exist at this coordinates
    ("I", 1) -> (column, row)
    """
    y = coor[1]
    x = coor[0]
    if type(x) == str:
        letters = string.ascii_uppercase
        return data[y][letters.index(x)] == "*"

    return data[y][x] == "*"


def ship_size(data, coor):
    """
    (list, tuple) -> (bool)

    Check if the ship exist at this coordinates
    and return it size

    >>> ship_size([[' ', ' ', '*', '*', ' ', ' ', ' ', ' ', ' ', ' '], [' ', ' ', ' ', ' ', ' ', '*', '*', '*', ' ', ' '], [' ', ' ', '*', '*', ' ', ' ', ' ', ' ', ' ', ' '], [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '], ['*', '*', '*', ' ', ' ', ' ', ' ', ' ', ' ', ' '], [' ', ' ', ' ', ' ', ' ', '*', ' ', ' ', ' ', ' '], ['*', '*', '*', '*', ' ', ' ', ' ', ' ', '*', ' '], [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', '*', ' '], [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '], ['*', ' ', ' ', '*', ' ', ' ', ' ', ' ', '*', ' ']], ("I", 8))
    2
    """

    if has_ship(data, coor):
        size = 1
        x = coor[1]
        y = index_of_letter(coor[0])
        if (y + 1 < 10 and has_ship(data, (y + 1, x))) or (y - 1 >= 0 and has_ship(data, (y - 1, x))):
            # horizontal
            for i in range(1, 9):
                if y-i >= 0 and has_ship(data, (y - i, x)):
                    size += 1
                else:
                    break

            for i in range(1, 9):
                if y+i < 10 and has_ship(data, (y + i, x)):
                    size += 1
                else:
                    break

        # vertical
        for i in range(1, 9):
            if x-i >= 0 and has_ship(data, (y, x - i)):
                size += 1
            else:
                break

        for i in range(1, 9):
            if x+i < 10 and has_ship(data, (y, x + i)):
                size += 1
            else:
                break

        return size

    return 0


def is_valid(data):
    """
    (data) -> (bool)

    Check if this field is filled by ships in right way
    There are must be 4: 1x1, 3: 1x2, 2: 1x3, 1: 1x4 ships
    and all of them can not touch anyone other
    """

    # check board size
    if len(data) != 10:
        return False
    for line in data:
        if len(line) != 10:
            return False

    letters = string.ascii_uppercase
    ships = [0, 0, 0, 0, 0]

    for i in range(10):
        for j in range(10):
            if has_ship(data, (letters[j], i)):
                size = ship_size(data, (letters[j], i))
                if size > 4:
                    return False
                ships[size] += 1

                horiz = False
                if has_ship(data, (j-1, i)) or has_ship(data, (j+1, i)):
                    horiz = True

                if horiz:
                    for z in range(j, j + size):
                        data[i][z] = " "
                else:
                    for z in range(i, i + size):
                        data[z][j] = " "

                if not check_ship_pos(data, i, j, size, horiz):
                    return False


    # Check number of ships
    if ships[1] < 4 or ships[2] < 3 or ships[3] < 2 or ships[4] < 1:
        return False

    return True


# Additional functions:

def field_to_str(data):
    """
    (data) -> (str)

    Transform data set to string that can be printed or displayed
    """
    result = ""
    for line in data:
        result += "".join(line) + "\n"

    return result


def generate_field():
    """
    () -> (data)

    Generate a random field with all ships in proper way
    """
    data = [[" "] * 10 for i in range(10)]
    ships = [4, 3, 3, 2, 2, 2, 1, 1, 1, 1]
    count = 0

    while count != 10:
        size = ships.pop(0)

        while True:
            horiz = random.choice([True, False])
            x = random.choice(range(0, 10))
            y = random.choice(range(0, 10))

            if (horiz and y+size > 9) or (not horiz and x+size > 9):
                continue

            if check_ship_pos(data, x, y, size, horiz):
                if horiz:
                    for i in range(y, y + size):
                        data[x][i] = "*"
                else:
                    for i in range(x, x + size):
                        data[i][y] = "*"

                break

        count += 1

    return data


# print(read_file("field.txt"))
# print(check_prop_place(read_file("field.txt"), 1, 6))
# print(check_ship_pos(read_file("field.txt"), 0, 0, 2, True))
# print(field_to_str(generate_field()))
# print(read_file("field.txt"))
# print(len(read_file("field.txt")))
# print(is_valid(read_file("field.txt")))
