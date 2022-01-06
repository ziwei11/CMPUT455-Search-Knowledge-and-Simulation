import random

class ZobristHash:
    def __init__(self, boardSize):
        self.board_index = boardSize * boardSize
        self.zobristhash_array = []
        for i in range(self.board_index):
            self.zobristhash_array.append([random.getrandbits(64) for j in range(3)])

    def hash(self, board):
        code = self.zobristhash_array[0][board[0]]
        for i in range(1, self.board_index):
            code = code ^ self.zobristhash_array[i][board[i]]
        return code