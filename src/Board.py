import pygame
from .Config import BLACK, RED, ROWS, COLUMNS, WHITE, SQUARE_SIZE
from .Checker import Checker
import src.King as King


class Board:
    board = []
    white_kings_left = 0
    black_kings_left = 0

    def __init__(self):
        self.board = []
        self.red_left = self.white_left = 12
        self.red_kings = self.white_kings = 0
        self.create_board()

    def draw_squares(self, win):
        win.fill(BLACK)
        for row in range(ROWS):
            for col in range(row % 2, COLUMNS, 2):
                pygame.draw.rect(win, RED, (row * SQUARE_SIZE, col * SQUARE_SIZE,
                                            SQUARE_SIZE, SQUARE_SIZE))

    def evaluate(self):
        return self.white_left - self.red_left + (self.white_kings * 0.5 - self.red_kings * 0.5)

    def get_all_pieces(self, color):
        pieces = []
        for row in self.board:
            for piece in row:
                if piece != 0 and piece.color == color:
                    pieces.append(piece)
        return pieces

    def move(self, piece, row, col):
        self.board[piece.row][piece.col], self.board[row][col] = self.board[row][col], self.board[piece.row][
            piece.col]
        piece.move(row, col)

        if type(piece) == Checker and (row == ROWS - 1 or row == 0):
            if piece.color == RED:
                self.black_kings_left += 1
            else:
                self.white_kings_left += 1
            self.board[row][col] = King.King(row, col, piece.color)

    def get_tile(self, row, col):
        return self.board[row][col]

    def get_possible_jumps(self, piece):
        jumps = {}
        all_rules = piece.jump_rules()
        for position in all_rules.keys():
            row, column = position
            if 0 <= row < ROWS and 0 <= column < COLUMNS and self.board[row][column] == 0:
                r, c = all_rules[position]
                if self.board[r][c] != 0 and self.board[r][c].color != piece.color:
                    jumps[position] = (r, c)
        return jumps

    def create_board(self):
        for row in range(ROWS):
            self.board.append([])
            for col in range(COLUMNS):
                if col % 2 == ((row + 1) % 2):
                    if row < 3:
                        self.board[row].append(Checker(row, col, WHITE))
                    elif row > 4:
                        self.board[row].append(Checker(row, col, RED))
                    else:
                        self.board[row].append(0)
                else:
                    self.board[row].append(0)

    def draw(self, win):
        self.draw_squares(win)
        for row in range(ROWS):
            for col in range(COLUMNS):
                piece = self.board[row][col]
                if piece != 0:
                    piece.draw(win)

    def remove(self, piece):
        self.board[piece.row][piece.col] = 0
        if piece.color == WHITE:
            self.white_left -= 1
        else:
            self.red_left -= 1

    def winner(self):
        if self.red_left <= 0:
            return WHITE
        elif self.white_left <= 0:
            return RED
        return None

    def get_valid_moves(self, piece):
        jumps = self.get_possible_jumps(piece)
        if jumps != {}:
            return jumps
        return self.get_possible_moves(piece)

    def get_possible_moves(self, piece):
        moves = {}
        for position in piece.move_rules():
            row, column = position
            if 0 <= row < ROWS and 0 <= column < COLUMNS:
                if self.board[row][column] == 0:
                    moves[position] = None
        return moves

    def _traverse_left(self, start, stop, step, color, left, skipped=[]):
        moves = {}
        last = []
        for r in range(start, stop, step):
            if left < 0:
                break
            current = self.board[r][left]
            if current == 0:
                if skipped and not last:
                    break
                elif skipped:
                    moves[(r, left)] = last + skipped
                else:
                    moves[(r, left)] = last

                if last:
                    if step == -1:
                        row = max(r - 3, 0)
                    else:
                        row = min(r + 3, ROWS)
                    moves.update(self._traverse_left(r + step, row, step, color, left - 1, skipped=last))
                    moves.update(self._traverse_right(r + step, row, step, color, left + 1, skipped=last))
                break
            elif current.color == color:
                break
            else:
                last = [current]

            left -= 1

        return moves

    def _traverse_right(self, start, stop, step, color, right, skipped=[]):
        moves = {}
        last = []
        for r in range(start, stop, step):
            if right >= COLUMNS:
                break

            current = self.board[r][right]
            if current == 0:
                if skipped and not last:
                    break
                elif skipped:
                    moves[(r, right)] = last + skipped
                else:
                    moves[(r, right)] = last

                if last:
                    if step == -1:
                        row = max(r - 3, 0)
                    else:
                        row = min(r + 3, ROWS)
                    moves.update(self._traverse_left(r + step, row, step, color, right - 1, skipped=last))
                    moves.update(self._traverse_right(r + step, row, step, color, right + 1, skipped=last))
                break
            elif current.color == color:
                break
            else:
                last = [current]

            right += 1

        return moves
