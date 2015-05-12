__author__ = 'Shahar Osovsky'


class LOP:
    SUCCESS = True
    FAIL = False

    # A constructor for a LOP object, initializing an empty list to be filled with tiles played
    def __init__(self):
        self.__tilesPlayed = list()

    # Printing the LOP according to it's order
    def __str__(self):
        print_LOP = ""
        if len(self.__tilesPlayed) > 0:
            for t in self.__tilesPlayed:
                print_LOP += str(t)
                if t != self.__tilesPlayed[len(self.__tilesPlayed) - 1]:
                    print_LOP += " "
        return print_LOP

    # Inserts the given tile to the given location if possible.
    # Returns 1 if attempt was successful, and -1 otherwise
    def human_insert(self, tile, location):
        lop_length = len(self.__tilesPlayed)
        if lop_length == 0:
            self.__tilesPlayed.append(tile)
        elif location in "sS":    # If the player wants to put the tile at the beginning
            if tile.get_side_A() == self.__tilesPlayed[0].get_side_A():
                self.__tilesPlayed.insert(0, tile.reverse_tile())
            elif tile.get_side_B() == self.__tilesPlayed[0].get_side_A():
                self.__tilesPlayed.insert(0, tile)
            else:
                return LOP.FAIL
        else:   # If the player wants to put the tile at the end
            if tile.get_side_A() == self.__tilesPlayed[lop_length - 1].get_side_B():
                self.__tilesPlayed.append(tile)
            elif tile.get_side_B() == self.__tilesPlayed[lop_length - 1].get_side_B():
                self.__tilesPlayed.append(tile.reverse_tile())
            else:
                return LOP.FAIL
        return LOP.SUCCESS

    # Inserts tile from the given tiles-list to the game using the easy algorithm.
    # Returns the index of the tile inserted if successful, and -1 otherwise
    def comp_easy_insert(self, tiles):
        tiles_length = len(tiles)
        for i in xrange(tiles_length):
            if self.insert_comp_tile(tiles[i]):
                return i
        return -1

    # Inserting a single tile to the board using the easy-computer algorithm, returning True if
    # the tile was placed legally, False otherwise
    def insert_comp_tile(self, tile):
        lop_length = len(self.__tilesPlayed)
        if tile.get_side_A() == self.__tilesPlayed[lop_length - 1].get_side_B():
            self.__tilesPlayed.append(tile)
        elif tile.get_side_A() == self.__tilesPlayed[0].get_side_A():
            self.__tilesPlayed.insert(0, tile.reverse_tile())
        elif tile.get_side_B() == self.__tilesPlayed[lop_length - 1].get_side_B():
            self.__tilesPlayed.append(tile.reverse_tile())
        elif tile.get_side_B() == self.__tilesPlayed[0].get_side_A():
            self.__tilesPlayed.insert(0, tile)
        else:
            return LOP.FAIL
        return LOP.SUCCESS

    # Returns True if there is a possible move with the given tile, False otherwise
    def possible_insert(self, tile):
        lop_length = len(self.__tilesPlayed)
        if lop_length == 0:
            return True
        if ((tile.get_side_A() == self.__tilesPlayed[lop_length - 1].get_side_B()) or
            (tile.get_side_A() == self.__tilesPlayed[0].get_side_A()) or
            (tile.get_side_B() == self.__tilesPlayed[lop_length - 1].get_side_B()) or
                (tile.get_side_B() == self.__tilesPlayed[0].get_side_A())):
            return True
        return False

    # Returns True if the given tile could be placed in the end of the board as is,
    # False otherwise
    def low_to_end(self, tile):
        lop_length = len(self.__tilesPlayed)
        return (tile.get_side_A() == self.__tilesPlayed[lop_length - 1].get_side_B())

    # Returns True if the given tile could be placed in the start of the board reversed,
    # False otherwise
    def low_to_start(self, tile):
        return (tile.get_side_A() == self.__tilesPlayed[0].get_side_A())

    # Returns True if the given tile could be placed in the end of the board reversed,
    # False otherwise
    def high_to_end(self, tile):
        lop_length = len(self.__tilesPlayed)
        return (tile.get_side_B() == self.__tilesPlayed[lop_length - 1].get_side_B())

    # Returns True if the given tile could be placed in the start of the board as is,
    # False otherwise
    def high_to_start(self, tile):
        return (tile.get_side_B() == self.__tilesPlayed[0].get_side_A())

    # Adding the given tile to the end of the LOP
    def add_to_end(self, tile):
        self.__tilesPlayed.append(tile)

    # Adding the given tile to the start of the LOP
    def add_to_start(self, tile):
        self.__tilesPlayed.insert(0, tile)

    # Returns the length of the this LOP
    def len(self):
        return len(self.__tilesPlayed)

    # Returns the tile at the given index in this LOP
    def get_tile_at_index(self, index):
        return self.__tilesPlayed[index]
