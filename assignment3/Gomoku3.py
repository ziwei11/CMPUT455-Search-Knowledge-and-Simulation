#!/usr/bin/python3
# Set the path to your python3 above

from gtp_connection import GtpConnection
import random
from board_util import GoBoardUtil
from board import GoBoard


class Gomoku():
    def __init__(self):
        """
        Gomoku player that selects moves randomly from the set of legal moves.
        Passes/resigns only at the end of the game.

        Parameters
        ----------
        name : str
            name of the player (used by the GTP interface).
        version : float
            version number (used by the GTP interface).
        """
        self.name = "GomokuAssignment3"
        self.version = 1.0
        self.simulation_number = 10   


    def get_move(self, board, color):
        self.board = board
        moves = self.board.rule_based_simulation(color)[1]
        best_move = 0
        best_score = -1
        for i in moves:
            score = self.simulate(board, i, color)
            if score > best_score:
                best_move = i
                best_score = score
        return best_move


    def simulate(self, board, first_move, color):
        win_number = 0
        draw_number = 0
        for i in range(self.simulation_number):
            board_copy = board.copy()
            board_copy.play_move(first_move, color)
            winner = board_copy.detect_five_in_a_row()
            while winner == 0 and len(board_copy.get_empty_points()) != 0:
                moves = board_copy.rule_based_simulation(board_copy.current_player)[1]
                random_move = random.choice(moves)
                board_copy.play_move(random_move, board_copy.current_player)
                winner = board_copy.detect_five_in_a_row()
            if winner == 0:
                draw_number += 1
            if winner == color:
                win_number += 1
        return win_number * (self.simulation_number + 1) + draw_number



def run():
    """
    start the gtp connection and wait for commands.
    """
    board = GoBoard(7)
    con = GtpConnection(Gomoku(), board)
    con.start_connection()


if __name__ == "__main__":
    run()
