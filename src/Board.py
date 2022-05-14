import pygame
import src.Checker as Checker
import src.Config as Config
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
        win.fill(Config.BLACK_TILES_COLOR)
        for row in range(Config.ROWS):
            for col in range(row % 2, Config.COLUMNS, 2):
                pygame.draw.rect(win, Config.WHITE_TILES_COLOR, (row * Config.SQUARE_SIZE, col * Config.SQUARE_SIZE,
                                            Config.SQUARE_SIZE, Config.SQUARE_SIZE))

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

        if type(piece) == Checker.Checker and (row == Config.ROWS - 1 or row == 0):
            if piece.color == Config.Pieces.BLACK:
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
            if 0 <= row < Config.ROWS and 0 <= column < Config.COLUMNS and self.board[row][column] == 0:
                r, c = all_rules[position]
                if self.board[r][c] != 0 and self.board[r][c].color != piece.color:
                    jumps[position] = (r, c)
        return jumps

    def create_board(self):
        for row in range(Config.ROWS):
            self.board.append([])
            for col in range(Config.COLUMNS):
                if col % 2 == ((row + 1) % 2):
                    if row < 3:
                        self.board[row].append(Checker.Checker(row, col, Config.Pieces.WHITE))
                    elif row > 4:
                        self.board[row].append(Checker.Checker(row, col, Config.Pieces.BLACK))
                    else:
                        self.board[row].append(0)
                else:
                    self.board[row].append(0)

    def draw(self, win):
        self.draw_squares(win)
        for row in range(Config.ROWS):
            for col in range(Config.COLUMNS):
                piece = self.board[row][col]
                if piece != 0:
                    piece.draw(win)

    def remove(self, piece):
        self.board[piece.row][piece.col] = 0
        if piece.color == Config.Pieces.WHITE:
            self.white_left -= 1
        else:
            self.red_left -= 1

    def winner(self):
        if self.red_left <= 0:
            return Config.Pieces.WHITE
        elif self.white_left <= 0:
            return Config.Pieces.BLACK
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
            if 0 <= row < Config.ROWS and 0 <= column < Config.COLUMNS:
                if self.board[row][column] == 0:
                    moves[position] = None
        return moves