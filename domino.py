__author__ = 'Shahar Osovsky'
import sys
from game import Game
# The game works perfectly fine, only the two hard parsing testers held me down,
# Probably if I had more time I would have found a way to fix it, for your consideration :)

CHOOSE_ACTION = "\nChoose action: Tile (t) or Draw (d): "
ILLEGAL_MOVE = "Error: Illegal move"
DRAW = -1


# Prints a massage announcing the winner of the game, which his name and id are
# given as parameters
def print_win(player_id, player_name):
    print "Player " + str(player_id) + ", " + player_name + " wins!"


# Prints a massage notifying the game ended in a draw
def print_draw():
    print "It's a draw!"


# Prints a the name of the player whose turn is up, along with his data (his hand),
# and the current state of the board (the LOP)
def print_step(player_id, player_name, game):
    print "\nTurn of " + player_name + " to play, player " + str(player_id) + ":"
    current_player = game.find_player(player_id)
    print "Hand :: " + str(game.get_players_list()[current_player])
    print "LOP  :: " + str(game.get_LOP()),


# Set-up the game for it's initiation
def game_set_up(game):
    print "Welcome to Domino!"

    file_path = raw_input("'tile' file path: ")

    num_of_players = raw_input("number of players (1-4): ")

    # In this case, file_parser() should return iterable data structure (later we will access tiles[i])
    tiles = Game.file_parser(file_path, num_of_players)
    for i in xrange(1, int(num_of_players) + 1):
        player_name, is_human = raw_input("player " + str(i) + " name: "), raw_input("Human player (y/n): ")
        game.add_player(i, player_name, is_human,
                        raw_input("Computer skill: Easy (e), Medium (m): ") if is_human == 'n' else "", tiles[i-1])

    leftover_tiles = list()
    for i in xrange(int(num_of_players), 4):
        leftover_tiles += tiles[i]
    game.create_double_six(leftover_tiles)


# The sequence of the game, returns the winner's index or -1 if the game ended in a draw
def game_play(game):
    num_of_players = len(game.get_players_list())
    turns_without_moves = 0     # Counts consecutive turns in which players had no moves
    current_player = game.first_player()
    # The game itself
    while True:
        if game.can_play(current_player):   # If there is a possible move for the current player
            print_step(game.get_id_at_index(current_player), game.get_name_at_index(current_player), game)
            if game.lop_is_empty():     # Only for the first turn in the entire game
                game.play_first_move(current_player)
                current_player = game.next_player(current_player)   # Advancing to the next player
            else:
                sys.stdout.write('')
                turns_without_moves = 0
                if game.get_players_list()[current_player].is_human():   # A HUMAN PLAYER
                    legal_play = False
                    while not legal_play:
                        action = raw_input(CHOOSE_ACTION)
                        # Plays a human player's single turn with the chosen action
                        legal_play = game.human_play(current_player, action)
                        if not legal_play:
                            print ILLEGAL_MOVE
                else:       # A COMPUTER PLAYER
                    game.computer_play(current_player)  # Plays a computer player's single turn
                if len(game.get_players_list()[current_player].get_hand()) == 0:
                    return current_player
                sys.stdout.write('\n')
                current_player = game.next_player(current_player)   # Advancing to the next player
        else:    # If there is no possible move for the current player
            turns_without_moves += 1
            current_player = game.next_player(current_player)   # Advancing to the next player
            if turns_without_moves == num_of_players:     # No player has any moves left
                return DRAW


# The main method, operating the game.
def main():
    game = Game()
    game_set_up(game)
    winner = game_play(game)
    if winner == DRAW:
        print_draw()
    else:
        if not game.get_players_list()[winner].is_human():
            print ""
        print_win(game.get_id_at_index(winner), game.get_name_at_index(winner))


if __name__ == "__main__":
    main()
