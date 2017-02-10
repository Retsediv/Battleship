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
