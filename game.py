__author__ = 'Shahar Osovsky'
from player import Player
from tile import Tile
from lop import LOP
from doubleSix import DoubleSix

COMMENT = "/"
COMMENT2 = "#"
STAR_COMMENT = "/*"
END_STAR_COMMENT = "*/"
QUOTE = '''"'''
NEW_LINE = "\n"
BLANK_SPACE = " "


class Game:

    HAND_SIZE = 7

    # A constructor for a Domino game object
    def __init__(self):
        self.__players = list()  # A list containing all the players in the game
        self.__lop = LOP()

    # Parsing the given file into lists of cards, which are the players' hands.
    # A function that is all but resistant to your tests 24,25 with Parsie the evil parser.
    # It's pretty complicated for people who don't know python very well to protect against
    # such a file (with comments which hide inside the lines of data)
    @staticmethod
    def file_parser(file_path, num_of_players):
        hands = [[0] * Game.HAND_SIZE, [0] * Game.HAND_SIZE, [0] * Game.HAND_SIZE, [0] * Game.HAND_SIZE]
        source_file = open(file_path)
        file_lines = source_file.readlines()
        counter = 0
        for i in xrange(len(file_lines)):
            index = 0
            if (file_lines[i].startswith(COMMENT)) or (file_lines[i].startswith(NEW_LINE)
                                                       or (file_lines[i].startswith(COMMENT2))
                                                       or (file_lines[i].startswith(QUOTE))):
                continue
            for tileStr in file_lines[i].split("-"):    # Separating the lines into tiles
                tileChars = tileStr.split(",")          # Parsing each tile
                if counter < int(num_of_players):
                    hands[counter][int(tileChars[0]) - 1] = Tile(int(tileChars[1]),
                                                                 int(tileChars[2])).order_values_in_tiles()
                else:
                    hands[counter][index] = Tile(int(tileChars[1]), int(tileChars[2])).order_values_in_tiles()
                    index += 1
            counter += 1
        return hands

    # Adds a new player to the game
    def add_player(self, player_id, name, is_human, skill, tiles):
        self.__players.append(Player(player_id, name, is_human, skill, tiles))

    # Returns the player with the given ID.
    def find_player(self, player_id):
        for p in xrange(len(self.__players)):
            if self.get_id_at_index(p) == player_id:
                return p

    # Returns this game's LOP (list of tiles)
    def get_LOP(self):
        return self.__lop

    # Returns a list of this game's players
    def get_players_list(self):
        return self.__players

    # Returns the index of the first player in the game
    def first_player(self):
        value = 0
        first = list()
        for p in xrange(len(self.__players)):
            if self.__players[p].find_max_tile_value() > value:
                value = self.__players[p].find_max_tile_value()
                first = [p]
            elif self.__players[p].find_max_tile_value() == value:
                first.append(p)
        if len(first) == 1:     # In case there is one maximal value
            return first[0]
        else:   # In case there is more than one maximal value, compares name lexicographically
            return self.first_lex_name(first)

    # Returns the index of the player who's name is first lexicographically, from the given index list
    def first_lex_name(self, index_list):
        first = index_list[0]
        for i in index_list:
            if self.get_name_at_index(i) < self.get_name_at_index(first):
                first = i
        return first

    # Return the index of the player that plays next, given the current player's index
    def next_player(self, current):
        if (current == len(self.__players) - 1):
            return 0
        else:
            return current + 1

    # Returns the ID of the player at the given index
    def get_id_at_index(self, index):
        return self.__players[index].get_id()

    # Returns the name of the player at the given index
    def get_name_at_index(self, index):
        return self.__players[index].get_name()

    # Creating a Double-Six for this game, containing the tiles given as parameter
    def create_double_six(self, tiles):
        self.__doubleSix = DoubleSix(tiles)

    # A single turn of a human player after choosing an action, returns True if the play was legal
    # and False otherwise
    # Assuming a move is possible, because can_play() method was ran before this
    def human_play(self, player_index, action):
        if action in "dD":  # In case the player wants to draw a card
            drawn_tile = self.__doubleSix.draw_tile()
            if drawn_tile is not None:  # Adding the drawn card to the current player's hand
                self.__players[player_index].add_tile_to_hand(drawn_tile)
            else:
                return LOP.FAIL
        else:   # In case the player wants to place a tile in the board
            # Asking the user for tile no' and location
            move = raw_input(Game.print_choose_tile(len(self.__players[player_index].get_hand()))).split(BLANK_SPACE)
            tile_index = int(move[0]) - 1
            location = move[1]
            if (len(self.__players[player_index].get_hand()) > tile_index)\
                    and (tile_index >= 0):      # Checking the tile no' is legal
                chosen_tile = self.__players[player_index].get_hand()[tile_index]
                played = self.__lop.human_insert(chosen_tile, location)
                if played == LOP.SUCCESS:   # If the tile was place legally on the board
                    self.__players[player_index].remove_tile_from_hand(tile_index)
                else:   # If the tile couldn't be places legally on the board
                    return LOP.FAIL
        return LOP.SUCCESS

    # A single turn of a computer player with the given index
    # Assuming a move is possible, because can_play() method was ran before this
    def computer_play(self, player_index):
        if self.__players[player_index].get_skill() in "eE":
            self.comp_easy_play(player_index)
        else:
            self.comp_medium_play(player_index)

    # A single turn of a computer player using an easy algorithm,
    # Assuming a move is possible, because can_play() method was ran before this
    def comp_easy_play(self, player_index):
        index = self.__lop.comp_easy_insert(self.__players[player_index].get_hand())
        if index >= 0:  # If a tile was place legally on the board
            self.__players[player_index].remove_tile_from_hand(index)
        else:   # If no tile could be placed legally on the board
            drawn_tile = self.__doubleSix.draw_tile()
            # Adding the drawn card to the current player's hand
            self.__players[player_index].add_tile_to_hand(drawn_tile)

    # A single turn of a computer player using a medium algorithm
    # Assuming a move is possible, because can_play() method was ran before this
    def comp_medium_play(self, player_index):
        probabilities_and_moves = list()    # a list of lists: [move_index, move_probability]
        for t in self.__players[player_index].get_hand():   # Filling the list with min-prob moves
            probabilities_and_moves.append(self.min_probability_move(t, player_index))
        if self.__doubleSix.len() > 0:
            probabilities_and_moves.append([-1, 2])     # The possibility of drawing a card
        min_move = Game.find_player_min_move(probabilities_and_moves)
        if min_move[0] == -1:   # Draw is the best move
            drawn_tile = self.__doubleSix.draw_tile()
            # Adding the drawn card to the current player's hand
            self.__players[player_index].add_tile_to_hand(drawn_tile)
        else:   # There is a possible placement for a tile (with good enough probability)
            if min_move[1] == 0:    # Lower-to-end
                self.__lop.add_to_end(self.__players[player_index].get_hand()[min_move[0]])
            elif min_move[1] == 1:    # Lower-to-start
                self.__lop.add_to_start(self.__players[player_index].get_hand()[min_move[0]].reverse_tile())
            elif min_move[1] == 2:    # Higher-to-end
                self.__lop.add_to_end(self.__players[player_index].get_hand()[min_move[0]].reverse_tile())
            else:   # (min_move[1] == 3) - Higher-to-start
                self.__lop.add_to_start(self.__players[player_index].get_hand()[min_move[0]])
            self.__players[player_index].remove_tile_from_hand(min_move[0])

    # Prints a massage to the player to choose a tile and a location to place it
    @staticmethod
    def print_choose_tile(tiles_num):
        return "Choose tile (1-" + str(tiles_num) + "), and place (Start - s, End - e): "

    # Returns True if the player, with the given index, has a possible move in the game,
    # and False otherwise
    def can_play(self, player_index):
        for t in self.__players[player_index].get_hand():
            if self.__lop.possible_insert(t):   # Checking possible moves on each tile in the hand
                return True
        if self.__doubleSix.len() > 0:
            return True
        return False

    #---------------- Medium Computer Player Methods -----------------#

    # Returns a list of type [tile_index, move_index, move_probability] holding the lowest
    # probability in the list given as parameter.
    # if the move is "draw" (-1) - then the tile_index will also be -1
    @staticmethod
    def find_player_min_move(probabilities_and_moves_list):
        player_min_move = [0, 0, 3]
        for p in xrange(len(probabilities_and_moves_list)):
            if probabilities_and_moves_list[p][1] < player_min_move[2]:
                player_min_move[0] = p
                player_min_move[1] = probabilities_and_moves_list[p][0]
                player_min_move[2] = probabilities_and_moves_list[p][1]
        if player_min_move[2] == 2:     # Draw is the best move
            player_min_move[0] = -1
        return player_min_move

    # Returns a list containing the number of tiles with each value (0-6) we do not know of
    def numbers_we_dont_know_of(self, player_index):
        numbers = [DoubleSix.APPEARANCES_OF_EACH_NUM] * Game.HAND_SIZE
        for i in xrange(self.__lop.len()):
            numbers[self.__lop.get_tile_at_index(i).get_side_A()] -= 1
            if (self.__lop.get_tile_at_index(i).get_side_A() !=
                    self.__lop.get_tile_at_index(i).get_side_B()):
                numbers[self.__lop.get_tile_at_index(i).get_side_B()] -= 1
        for i in xrange(len(self.__players[player_index].get_hand())):
            numbers[self.__players[player_index].get_hand()[i].get_side_A()] -= 1
            if (self.__players[player_index].get_hand()[i].get_side_A() !=
                    self.__players[player_index].get_hand()[i].get_side_B()):
                numbers[self.__players[player_index].get_hand()[i].get_side_B()] -= 1
        return numbers

    # Returns a list of size 2, containing a number (0-3) representing one of the four
    # types of assignments possible in the game (cell 0), and the probability of the other players
    # to place a tile in the board if this assignment is done (cell 1).
    def min_probability_move(self, tile, player_index):
        num_of_tiles_unknown = DoubleSix.TOTAL_NUM_OF_TILES - \
            self.__lop.len() - len(self.__players[player_index].get_hand())
        numbers_unknown = self.numbers_we_dont_know_of(player_index)
        prob = list()
        if self.__lop.low_to_end(tile):
            prob.append(float(numbers_unknown[tile.get_side_B()]) / num_of_tiles_unknown)
        else:
            prob.append(3)
        if self.__lop.low_to_start(tile):
            prob.append(float(numbers_unknown[tile.get_side_B()]) / num_of_tiles_unknown)
        else:
            prob.append(3)
        if self.__lop.high_to_end(tile):
            prob.append(float(numbers_unknown[tile.get_side_A()]) / num_of_tiles_unknown)
        else:
            prob.append(3)
        if self.__lop.high_to_start(tile):
            prob.append(float(numbers_unknown[tile.get_side_A()]) / num_of_tiles_unknown)
        else:
            prob.append(3)
        return Game.min_prob_index(prob)

    # returning a list containing the index with the smallest probability (cell 0) and the
    # smallest probability (cell 1)
    @staticmethod
    def min_prob_index(prob_list):
        min_prob_index_list = [0, 3]
        for i in xrange(len(prob_list)):
            if prob_list[i] < min_prob_index_list[1]:
                min_prob_index_list[0] = i
                min_prob_index_list[1] = prob_list[i]
        return min_prob_index_list

    # Returns True if the LOP is empty, False otherwise
    def lop_is_empty(self):
        return (self.__lop.len() == 0)

    def play_first_move(self, player_index):
        print ""
        self.__lop.add_to_end(self.__players[player_index].get_hand()[0])
        self.__players[player_index].remove_tile_from_hand(0)
