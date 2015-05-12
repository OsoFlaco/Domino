__author__ = 'Shahar Osovsky'
import copy


class Player:

    def __init__(self, player_id, name, is_human, skill, tiles):
        self.__hand = copy.copy(tiles)
        if is_human in "yY":
            self.__is_human = True
        else:
            self.__is_human = False
        self.__id = player_id
        self.__name = name
        self.__skill = skill

    # Prints this player's hand, each tile printed in ascending order
    def __str__(self):
        print_hand = ""
        if len(self.__hand) > 0:
            for t in self.__hand:
                print_hand += (str(t))
                if t != self.__hand[len(self.__hand) - 1]:
                    print_hand += " "
        return print_hand

    # Returns the value of the most-valuable tile in this player's hand
    def find_max_tile_value(self):
        max_value = 0
        for t in self.__hand:
            if t.get_value() > max_value:
                max_value = t.get_value()
        return max_value

    # Adds the given tile to the player's hand
    def add_tile_to_hand(self, tile):
        self.__hand.append(tile)

    # Removes the tile that is at the given index in the player's hand
    def remove_tile_from_hand(self, tile_index):
        self.__hand.pop(tile_index)

    # Returns this player's name
    def get_name(self):
        return self.__name

    # Returns this player's id
    def get_id(self):
        return self.__id

    # Returns this player's skill
    def get_skill(self):
        return self.__skill

    # Returns True if this player is human, False otherwise
    def is_human(self):
        return self.__is_human

    # Returns this player's hand (a list of tiles)
    def get_hand(self):
        return self.__hand
