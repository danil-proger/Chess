import pygame
from .Config import RED, WHITE, BLUE, SQUARE_SIZE, ROWS, COLUMNS, POSSIBLE_MOVE_COLOR, VALID_MOVE_MARK_RADIUS
from src.Board import Board

class Game:
    forced_to_take = set()
    selected = None
    valid_moves = {}
    turn = RED
    board = Board()

    def __init__(self, win):
        self._init()
        self.win = win

    def update(self):
        self.board.draw(self.win)
        self.draw_valid_moves(self.valid_moves)
        pygame.display.update()

    def _init(self):
        self.selected = None
        self.turn = RED
        self.valid_moves = {}

    def winner(self):
        return self.board.winner()

    def reset(self):
        self._init()

    def select(self, row, col):
        if self.selected:
            result = self._move(row, col)
            if not result:
                self.selected = None
                self.valid_moves.clear()
                self.select(row, col)
        piece = self.board.get_tile(row, col)
        if piece != 0 and piece.color == self.turn:
            self.selected = piece
            if not len(self.forced_to_take) == 0:
                if piece in self.forced_to_take:
                    self.valid_moves = self.board.get_valid_moves(piece)
                else:
                    self.valid_moves.clear()
            else:
                self.valid_moves = self.board.get_valid_moves(piece)
            return True

        return False

    def _move(self, row, col):
        tile = self.board.get_tile(row, col)
        if self.selected and tile == 0 and (row, col) in self.valid_moves:
            piece_type_before_move = type(self.selected)
            self.board.move(self.selected, row, col)
            taken = self.valid_moves[(row, col)]
            if taken:
                self.if_taken(taken, row, col, piece_type_before_move)
            else:
                self.change_turn()
            return True
        return False

    def draw_valid_moves(self, moves):
        for move in moves:
            row, column = move
            pygame.draw.circle(self.win, POSSIBLE_MOVE_COLOR, (
                column * SQUARE_SIZE + SQUARE_SIZE // 2,
                row * SQUARE_SIZE + SQUARE_SIZE // 2), VALID_MOVE_MARK_RADIUS)

    def change_turn(self):
        self.valid_moves.clear()
        self.forced_to_take.clear()
        if self.turn == RED:
            self.turn = WHITE
        else:
            self.turn = RED
        self.find_forced_to_take_pieces()

    def get_board(self):
        return self.board

    def ai_move(self, board):
        self.board = board
        self.change_turn()

    def forced_take(self, piece):
        self.valid_moves = {}
        self.forced_to_take.add(piece)

    def find_forced_to_take_pieces(self):
        for row in range(ROWS):
            for column in range(COLUMNS):
                piece = self.board.get_tile(row, column)
                if piece != 0 and self.board.get_possible_jumps(piece) != {} and piece.color == self.turn:
                    self.forced_to_take.add(piece)

    def if_taken(self, taken, row, column, piece_type_before_move):
        r, c = taken
        taken_piece = self.board.get_tile(r, c)
        self.board.remove(taken_piece)
        piece = self.board.get_tile(row, column)
        if type(piece) == piece_type_before_move and self.board.get_possible_jumps(piece) != {}:
            self.forced_take(piece)

        else:
            self.change_turn()
