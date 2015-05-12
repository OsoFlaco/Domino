__author__ = 'Shahar Osovsky'


# A class representing the deck of domino tiles
class DoubleSix:
    #Constants:
    APPEARANCES_OF_EACH_NUM = 7
    TOTAL_NUM_OF_TILES = 28

    # A constructor for a Double-Six object, receiving a list of tiles as parameter
    # and fills it's list with these tiles
    def __init__(self, tiles):
        self.__doubleSix = list()
        for t in tiles:
            self.add_tile(t)

    # Drawing a tile from the double-six
    def draw_tile(self):
        if (len(self.__doubleSix) > 0):
            return self.__doubleSix.pop(0)
        else:
            return None

    # Adding a given to the double-six
    def add_tile(self, tile):
        self.__doubleSix.append(tile)

    # Prints the double-six deck
    def print_double_six(self):
        if len(self.__doubleSix) == 0:
            print ""
        for t in self.__doubleSix:
            print t

    # Returns the length of the this Double-Six
    def len(self):
        return len(self.__doubleSix)
