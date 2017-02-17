class Ship:
    """Class represent ships in the field"""

    def __init__(self, length, bow, horizontal=True):
        """ (Ship, int, tuple, bool) -> NoneType
        Init new Ship with it's length(tuple like a (1, 2) or (4, 1)), direction(horizontal as primary),
          coordinates(top-left side) and fill list of hit as False for the start
        """
        self.horizontal = horizontal
        self.bow = bow
        self.__length = length
        self.__hit = [False] * max(length)

    def shoot_at(self, coordinates):
        """ (Ship, tuple) -> (bool)
        Shoot at the ship and check if on this coordinates is this ship set it in hit list
        """
        try:
            if self.horizontal:
                self.__hit[coordinates[1] - self.bow[1]] = True
            else:
                self.__hit[coordinates[0] - self.bow[0]] = True

            return True
        except IndexError:
            return False

    def is_shot_at(self, coordinates):
        """ (Field, tuple) -> (bool)
        Check if you had already shot at this coordinates by ship
        """
        try:
            if self.horizontal:
                return self.__hit[coordinates[1] - self.bow[1]]
            else:
                return self.__hit[coordinates[0] - self.bow[0]]

        except Exception:
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
        self.__ships = self.generate_field()

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

    @staticmethod
    def check_ship_pos(data, x, y, size, horizontal):
        """ (data, int, int, int, bool) -> (bool)
        Check if you could put ship at this coordinates
        """
        if horizontal:
            for i in range(y, y + size):
                if not Field.check_prop_place(data, x, i):
                    return False
            return True
        else:
            for i in range(x, x + size):
                if not Field.check_prop_place(data, i, y):
                    return False
            return True

    def generate_field(self):
        """ () -> (data)
        Generate a random field with all ships in proper way
        """
        import random
        field = [[None] * 10 for _ in range(10)]
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
                        ship = Ship((1, size), (x, y))
                        for i in range(y, y + size):
                            field[x][i] = ship
                    else:
                        ship = Ship((size, 1), (x, y), horizontal=False)
                        for i in range(x, x + size):
                            field[i][y] = ship

                    break

        return field

    # Field output
    def field_without_ships(self):
        """ (Field) -> (str)
        Return string that display only cells which are already shot
          "■" -> shot at ship
          " " -> not shot
          "*" -> shot, but empty(no any ship here)
        """
        # output = ""
        output = []

        for line in self.__ships:
            out_line = []
            for ship_i in range(len(line)):
                if isinstance(line[ship_i], Ship):
                    out_line.append("■" if line[ship_i].is_shot_at((self.__ships.index(line), ship_i)) else " ")
                else:
                    out_line.append(line[ship_i] if (line[ship_i] is not None) else " ")

            output.append(out_line)

        return Field.beauty_field(output)

    def field_with_ships(self):
        """ (Field) -> (str)
        Transform data set to string that can be printed or displayed
        """
        result = ""
        for line in self.__ships:
            for i in line:
                if i is None:
                    i = " "
                if isinstance(i, Ship):
                    i = "□"  # Icons for ships ■ □

                result += i
            result += "\n"

        return result

    @staticmethod
    def beauty_field(board):
        """ (list) -> (str)
        Make beautiful board(with numbers, letters and cells)
        """
        board = [[str(i+1) + ("" if i+1 == 10 else " ")] + board[i] for i in range(len(board))]
        board.insert(0, ["  ", "A", "B", "C", "D", "E", "F", "G", "H", "I", "J"])
        for line in range(len(board)):
            for i in range(len(board[line])):
                board[line].insert(2*i+1, "|")
            board[line].append("\n")

        return "".join(["".join(line) for line in board])

    # Shooting!
    def shoot_at(self, coordinates):
        """ (Field, tuple) -> (bool)
        Shoot at specific coordinates and return True if there is a ship and
          you had not shot here yet
        """
        if isinstance(self.__ships[coordinates[0]][coordinates[1]], Ship):
            # Check if not already shot is at Ship class
            return self.__ships[coordinates[0]][coordinates[1]].shoot_at(coordinates)

        self.__ships[coordinates[0]][coordinates[1]] = "*"
        return False


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
        self.score = 0

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

        while True:
            try:
                coordinates = input()
                row = int(coordinates[1:]) - 1  # because zero-indexation
                column = index_of_letter(coordinates[0].upper())
                if 0 <= row <= 9 and 0 <= column <= 9:
                    break
                else:
                    print("Coordinates must be from A1 ... to ... J10. \nTry one more:")
            except Exception:
                print("Coordinates must be from A1 ... to ... J10. \nTry one more:")

        return row, column


if __name__ == "__main__":
    pass
    # field = Field()
    # print(field.shoot_at((0, 0)))
    # print(field.shoot_at((1, 0)))
    # print(field.field_without_ships())
    # print(field.field_with_ships())
