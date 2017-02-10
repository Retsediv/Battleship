from core import Ship, Field, Player


class Game:
    """Combine all game classes and provide logic for play game"""

    def __init__(self, names, current_player=0):
        """ (Game) -> NoneType
        Create a instance of Game class, two players(with names),
          generate fields for them and set current player(index 0 or 1))
        """
        self.fields = [Field(), Field()]
        self.players = [Player(names[0]), Player(names[1])]
        self.currentPlayer = current_player

    def read_position(self):
        """ (Game) -> (tuple)
        Read coordinates for shooting from player and return converted tuple of them
          "converted": A10 -> (9, 0)
        """
        return self.players[self.currentPlayer].read_position()

    def field_without_ships(self, index):
        """ (Game, int) -> (str)
        Return string than represent field(without any ships) by specific index
        """
        return self.fields[index].field_without_ships()

    def field_with_ships(self, index):
        """ (Game, int) -> (str)
        Return string than represent field(with all ships) by specific index
        """
        return self.fields[index].field_with_ships()

    def play(self):
        """ (Game) -> (str)
        Play function that return name of winner
        """

        def another_player(index):
            return 1 if index == 0 else 0

        print("Game Battleship")
        while True:  # while is not a winner
            # Show field of another player
            another_player_index = another_player(self.currentPlayer)

            while True:
                print("Field of " + str(another_player_index + 1) + " player")
                print(self.field_without_ships(another_player_index))

                # Read coordinates for shooting
                print("Player " + str(self.currentPlayer + 1) + " enter coordinates: ")
                coordinates = self.read_position()

                # Shoot
                shot = self.fields[another_player_index].shoot_at(coordinates)
                if not shot:
                    break
                else:
                    print("Good job! You can shout one more")

                print(6)

            self.currentPlayer = another_player_index


game = Game(["Andrii", "Joe"])
game.play()
