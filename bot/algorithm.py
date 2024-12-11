from copy import deepcopy
import src.Config as Config


def minimax(position, depth, max_player, game):
    if depth == 0 or position.winner() is not None:
        return position.evaluate(), position

    if max_player:
        max_eval = float('-inf')
        best_move = None
        for move in get_all_moves(position, Config.Pieces.WHITE, game):
            evaluation = minimax(move, depth - 1, False, game)[0]
            max_eval = max(max_eval, evaluation)
            if max_eval == evaluation:
                best_move = move

        return max_eval, best_move
    else:
        min_eval = float('inf')
        best_move = None
        for move in get_all_moves(position, Config.Pieces.BLACK, game):
            evaluation = minimax(move, depth - 1, True, game)[0]
            min_eval = min(min_eval, evaluation)
            if min_eval == evaluation:
                best_move = move

        return min_eval, best_move


def simulate_move(piece, move, board, game, skip):
    board.move(piece, move[0], move[1])
    if skip:
        t = board.get_tile(skip[0], skip[1])
        board.remove(t)
        zxc = board.get_possible_jumps(piece)
        if zxc:
            simulate_move(piece, list(zxc.keys())[0], board, game, list(zxc.values())[0])

    return board


def get_all_moves(board, color, game):
    moves = []
    forced_to_take = set()
    for piece in board.get_all_pieces(color):
        if board.get_possible_jumps(piece) != {}:
            forced_to_take.add(piece)

    for piece in board.get_all_pieces(color):
        if piece in forced_to_take or len(forced_to_take) == 0:
            valid_moves = board.get_valid_moves(piece)
            for move, skip in valid_moves.items():
                temp_board = deepcopy(board)
                temp_piece = temp_board.get_tile(piece.row, piece.col)
                new_board = simulate_move(temp_piece, move, temp_board, game, skip)
                moves.append(new_board)

    return moves