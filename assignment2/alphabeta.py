from board import GoBoard
from board_util import GoBoardUtil
from transpositiontable import TranspositionTable
from zobristhash import ZobristHash

def alphabeta(state: GoBoard, alpha, beta, transposition: TranspositionTable,
              hasher: ZobristHash):
    code = hasher.hash(GoBoardUtil.get_oneD_board(state))
    result = transposition.lookup(code)
    if result != None:
        return result
    if state.game_over():
        result = (state.evaluate(), None)
        storeResult(transposition, code, result)
        return result

    moves = state.best_move()
    best_move = moves[0]

    for move in moves:
        state.play_move(move, state.current_player)
        value, _ = alphabeta(state, -beta, -alpha, transposition, hasher)
        value = -value
        if value > alpha:
            alpha = value
            best_move = move
        state.undo_move(move)
        if value >= beta:
            result = beta, move
            storeResult(transposition, code, result)
            return result

    result = alpha, best_move
    storeResult(transposition, code, result)
    return result

def call_alphabeta(rootState, transposition, hasher):
    return alphabeta(rootState, -10000, 10000, transposition, hasher)

def storeResult(transposition, code, result):
    transposition.store(code, result)
    return result
