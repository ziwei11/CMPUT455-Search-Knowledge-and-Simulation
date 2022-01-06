from board_util import GoBoardUtil, EMPTY
import random


class NodeData:
    def __init__(self, winner, moves, visited, wins):
        self.winner = winner
        self.moves = moves
        self.wins = wins
        self.visited = visited


class MCTS:
    def __init__(self):
        self.numSimulation = 1000
        self.dictionary = dict()
        self.initial_lines()

    def get_best_move(self, board, moves):
        best_move = 0
        high = 0
        toplay = board.current_player
        for move in moves:
            board.board[move] = toplay
            hash_key = hash(board)
            board.board[move] = EMPTY
            if hash_key not in self.dictionary:
                continue
            data = self.dictionary[hash_key][toplay]
            if data == None:
                continue
            w_rate = data.wins / data.visited
            if w_rate > high:
                best_move = move
                high = w_rate
        if best_move == 0:
            return random.choice(moves)
        return best_move

    def initial_lines(self):
        self.lines = []
        self.diag1Dict = {}
        self.diag2Dict = {}
        self.rows = []
        first = 9
        for i in range(7):
            new_line = []
            for j in range(7):
                a = first + j
                new_line.append(a)
            self.rows.append(new_line)
            first = first + 8
        for row in self.rows:
            self.lines.append(row)

        self.cols = []
        second = 9
        for i in range(7):
            new_line = []
            b = second
            for j in range(7):
                new_line.append(b)
                b = b + 8
            self.cols.append(new_line)
            second = second + 1
        for col in self.cols:
            self.lines.append(col)

        self.diags1 = []
        third = 9
        begin = 7
        for i in range(7):
            new_line = []
            c = third
            for j in range(begin):
                new_line.append(c)
                c = c + 9
            self.diags1.append(new_line)
            begin = begin - 1
            third = third + 1
            
        fourth = 17
        begin = 6
        for i in range(6):
            new_line = []
            d = fourth
            for j in range(begin):
                new_line.append(d)
                d = d + 9
            self.diags1.append(new_line)
            begin = begin - 1
            fourth = fourth + 8
        for i in range(len(self.diags1)):
            diag = self.diags1[i]
            self.lines.append(diag)
            for j in diag:
                self.diag1Dict[j] = i

        self.diags2 = []
        fifth = 9
        begin = 1
        for i in range(7):
            new_line = []
            e = fifth
            for j in range(begin):
                new_line.append(e)
                e = e + 7
            self.diags2.append(new_line)
            begin = begin + 1
            fifth = fifth + 1
            
        sixth = 23
        begin = 6
        for i in range(6):
            new_line = []
            f = sixth
            for j in range(begin):
                new_line.append(f)
                f = f + 7
            self.diags2.append(new_line)
            begin = begin - 1
            sixth = sixth + 8
        for i in range(len(self.diags2)):
            diag = self.diags2[i]
            self.lines.append(diag)
            for j in diag:
                self.diag2Dict[j] = i

    def get_node(self, hash_key, toplay):
        if hash_key not in self.dictionary:
            self.dictionary[hash_key] = [None, None, None]
        data = self.dictionary[hash_key][toplay]
        if data == None:
            data = NodeData()
            self.dictionary[hash_key][toplay] = data
        return data

    def simulation(self, board):
        toplay = board.current_player
        fmoves, winner = self.compute_move(board, toplay)
        if winner != -1:
            return random.choice(fmoves)
        if len(fmoves) == 1:
            return fmoves[0]
        i = 0
        while i < self.numSimulation:
            boardCopy = board.copy()
            fmove = random.choice(fmoves)
            boardCopy.play_move_gomoku(fmove, boardCopy.current_player)
            hash_key = hash(boardCopy)
            winner = self.simulate(boardCopy)
            data = self.get_node(hash_key, toplay)
            data.visited += 1
            if winner == toplay:
                data.wins += 1
        return self.get_best_move(board, fmoves)

    def simulate(self, board):
        while True:
            hash_key = hash(board)
            toplay = board.current_player
            if hash_key not in self.dictionary:
                self.dictionary[hash_key] = [None, None, None]
            if self.dictionary[hash_key][toplay] == None:
                moves, winner = self.compute_move(board, toplay)
                data = NodeData(winner, moves)
                self.dictionary[hash_key][toplay] = data
            data = self.dictionary[hash_key][toplay]
            if data.winner == -1:   # not win yet
                # randomly make a move
                move = random.choice(data.moves)
                board.board[move] = toplay
                board.current_player = GoBoardUtil.opponent(toplay)
            else:
                data.visited += 1
                if toplay == data.winner:
                    data.wins += 1
                return data.winner

    def compute_move(self, board, toplay):
        legal_moves = GoBoardUtil.generate_legal_moves_gomoku(board)
        if len(legal_moves) == 0:
            return None, EMPTY
        end, winner = board.check_game_end_gomoku()
        if end:
            return None, winner
        opponent = GoBoardUtil.opponent(toplay)
        n_moves = []
        for move in legal_moves:
            board.board[move] = toplay
            lines = self.get_corresponding_lines(move)
            if self.win_move(1, board, toplay, lines):
                return [move], toplay
            if self.win_move(1, board, opponent, lines):
                return [move], -1
            if self.win_move(2, board, toplay, lines):
                n_moves.append(move)
            if self.win_move(2, board, opponent, lines):
                return [move], -1
            board.board[move] = EMPTY
        if len(n_moves) != 0:
            return n_moves, toplay
        return legal_moves, -1

    def win_move(self, choice, board, toplay, lines):
        if choice == 1:
            for line in lines:
                for i in range(len(line) - 4):
                    count = 0
                    for j in range(i, i + 5):
                        pos = line[j]
                        if board.board[pos] == toplay:
                            count += 1
                    if count == 5:
                        return True
            return False
        if choice == 2:
            for line in lines:
                for i in range(len(line) - 5):
                    if board.board[line[i]] != EMPTY or board.board[line[i + 5]] != EMPTY:
                        continue
                    count = 0
                    for j in range(i + 1, i + 5):
                        pos = line[j]
                        if board.board[pos] == toplay:
                            count += 1
                    if count == 4:
                        return True
            return False    

    def get_corresponding_lines(self, pos):
        diag1 = self.diags1[self.diag1Dict[pos]]
        diag2 = self.diags2[self.diag2Dict[pos]]
        row = self.rows[pos // 8 - 1]
        col = self.cols[pos % 8 - 1]
        lines = [row, col, diag1, diag2]
        return lines
