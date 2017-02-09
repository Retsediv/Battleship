class Ship:
    """
    Class represent ships in the field
    """

    def __init__(self, length, bow, horizontal=True):
        """ (Ship, int, tuple, bool) -> NoneType
        Init new Ship with it's length(tuple like a (1, 2) or (4, 1)), direction(horizontal as primary),
          coordinates(top-left side) and fill list of hit as False for the start
        """
        self.length = length
        self.horizontal = horizontal
        self.bow = bow
        self.hit = [False] * max(length)

    def shoot_at(self, coordinates):
        """ (Player, tuple) -> (bool)
        Shoot at the ship and check if on this coordinates is this ship set it in hit list
        """
        if self.horizontal and coordinates[0] == self.bow[0] and \
                (self.bow[1] <= coordinates[1] < self.bow[1] + self.length[1]) and self.hit[
                    coordinates[1] - self.bow[1]] != True:
            self.hit[coordinates[1] - self.bow[1]] = True
            return True

        elif not self.horizontal and coordinates[1] == self.bow[1] and \
                (self.bow[0] <= coordinates[0] < self.bow[0] + self.length[0]) and self.hit[
                    coordinates[0] - self.bow[0]] != True:
            self.hit[coordinates[0] - self.bow[0]] = True
            return True

        return False


class Field:
    """
    Field with ships which gives possibility to generate a field,
      shoot at some coordinates and write out a field for user
    """
    def __init__(self):
        """ (Field) -> NoneType
        Generate field with random positioned ships
          ships are represented as Ship object
          empty spaces as None type
        """
        self.ships = self.generate_field()

    # Field generation
    @staticmethod
    def check_prop_place(data, x, y):
        """ (data, int, int) -> (bool)
        Check if this field not border with any ships
        """

        d = [(1, 0), (1, -1), (1, 1), (0, -1), (0, 1), (-1, 0), (-1, -1), (-1, 1)]
        for delta in d:
            dx = delta[0]
            dy = delta[1]

            if 0 <= x + dx < 10 and 0 <= y + dy < 10:
                if data[x + dx][y + dy] is not None:
                    return False

        return True

    def check_ship_pos(self, data, x, y, size, horizontal):
        """ (data, int, int, int, bool) -> (bool)
        Check if you could put ship at this coordinates
        """
        if horizontal:
            for i in range(y, y + size):
                if not self.check_prop_place(data, x, i):
                    return False
            return True
        else:
            for i in range(x, x + size):
                if not self.check_prop_place(data, i, y):
                    return False
            return True

    def generate_field(self):
        """ () -> (data)
        Generate a random field with all ships in proper way
        """
        import random
        field = [[None] * 10 for i in range(10)]
        ships = [4, 3, 3, 2, 2, 2, 1, 1, 1, 1]

        while ships:
            size = ships.pop(0)

            while True:
                horiz = random.choice([True, False])
                x = random.choice(range(0, 10))
                y = random.choice(range(0, 10))

                if (horiz and y + size > 9) or (not horiz and x + size > 9):
                    continue

                if self.check_ship_pos(field, x, y, size, horiz):
                    if horiz:
                        for i in range(y, y + size):
                            field[x][i] = "x"
                    else:
                        for i in range(x, x + size):
                            field[i][y] = "x"

                    break

        return field

    # Field presentation
    def __str__(self):
        """ (Field) -> (str)
        Transform data set to string that can be printed or displayed
        """
        result = ""
        for line in self.ships:
            for i in line:
                if i is None:
                    i = " "
                result += i
            result += "\n"

        return result

    # Shooting !!!

f = Field()
print(f)


class Player:
    """
    Class represent player(with field name) and gives possibility
      to read coordinates he wrote
    """

    def __init__(self, name):
        """ (Player, str) -> NoneType
        Init Player with specific name
        """
        self.__name = name

    def read_position(self):
        """ (Player) -> (tuple(int, int))
        Read coordinates from input like a "B10" and
          return tuple with them with zero indexation (1, 9)
        """

        def index_of_letter(let):
            """ (str) -> (int)
            Get index of letter in alphabet
            """
            import string
            letters = string.ascii_uppercase
            return letters.index(let)

        coordinates = input()
        row = int(coordinates[1:]) - 1  # because zero-indexation
        column = index_of_letter(coordinates[0])

        return row, column
