__author__ = 'Shahar Osovsky'


# A class representing a Tile object in the game of Domino
class Tile(object):
    # Possible values for each tile's sides
    VALUES = {0, 1, 2, 3, 4, 5, 6}
    DOUBLE_VALUE = 12

    # A constructor for a Tile object for the game of Domino, receiving it's 2 values as arguments
    def __init__(self, valueA, valueB):
        self.__sideA = 0
        self.__sideB = 0
        self.__hidden = False
        if (type(valueA) == int) and (valueA in Tile.VALUES):
            self.__sideA = valueA
        if (type(valueB) == int) and (valueB in Tile.VALUES):
            self.__sideB = valueB

    # Returns a reversed version of this tile (with it's sides switched)
    def reverse_tile(self):
        return Tile(self.__sideB, self.__sideA)

    # Reverses this tile if it's left value is higher than it's right value, and returns it
    def order_values_in_tiles(self):
        if self.__sideA > self.__sideB:
            self.__sideA, self.__sideB = self.__sideB, self.__sideA
        return self

    # Returns the "value" of the tile, meaning the sum of it's two sides, and if it happen
    # to be a "double" (both sides are equal) than additional bonus is added to it's sum
    def get_value(self):
        value = self.__sideA + self.__sideB
        if (self.__sideA == self.__sideB):
            value += Tile.DOUBLE_VALUE
        return value

    # Returns this tile's left value
    def get_side_A(self):
        return self.__sideA

    # Returns this tile's right value
    def get_side_B(self):
        return self.__sideB

    # Overriding the __str__ of the object to print it's values in ascending order
    def __str__(self):
        return "[" + str(self.__sideA) + ":" + str(self.__sideB) + "]"
