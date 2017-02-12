from core import Ship, Field, Player


class Game:
    """Combine all game classes and provide logic for play game"""

    def __init__(self, names, current_player=0):
        """ (Game) -> NoneType
        Create a instance of Game class, two players(with names),
          generate fields for them and set current player(index 0 or 1))
        """
        self.__fields = [Field(), Field()]
        self.__players = [Player(names[0]), Player(names[1])]
        self.__currentPlayer = current_player

    def read_position(self):
        """ (Game) -> (tuple)
        Read coordinates for shooting from player and return converted tuple of them
          "converted": A10 -> (9, 0)
        """
        return self.__players[self.__currentPlayer].read_position()

    def field_without_ships(self, index):
        """ (Game, int) -> (str)
        Return string than represent field(without any ships) by specific index
        """
        return self.__fields[index].field_without_ships()

    def field_with_ships(self, index):
        """ (Game, int) -> (str)
        Return string than represent field(with all ships) by specific index
        """
        return self.__fields[index].field_with_ships()

    def detect_winner(self):
        pass

    def play(self):
        """ (Game) -> (str)
        Play function that return name of winner
        """

        def another_player(index):
            return 1 if index == 0 else 0

        print("Game Battleship")
        while self.__players[self.__currentPlayer].score != 20:  # while is not a winner
            another_player_index = another_player(self.__currentPlayer)

            while True:  # While player does't miss

                # Show field of another player
                print("Field of " + str(another_player_index + 1) + " player")
                print(self.field_without_ships(another_player_index))

                # Read coordinates for shooting
                print("Player " + str(self.__currentPlayer + 1) + " enter coordinates: ")
                coordinates = self.read_position()

                # Shoot
                shot = self.__fields[another_player_index].shoot_at(coordinates)
                if not shot:
                    break
                else:
                    print("Good job! You can shout one more")
                    self.__players[self.__currentPlayer].score += 1

                print()

            self.__currentPlayer = another_player_index
