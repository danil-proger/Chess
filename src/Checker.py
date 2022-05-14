import pygame
import src.Config as Config


class Checker:
    def __init__(self, row, col, color):
        self.row = row
        self.col = col
        self.color = color
        self.king = False
        self.x = 0
        self.y = 0
        self.calc_pos()

    def calc_pos(self):
        self.x = Config.SQUARE_SIZE * self.col + Config.SQUARE_SIZE // 2
        self.y = Config.SQUARE_SIZE * self.row + Config.SQUARE_SIZE // 2

    def move_rules(self):
        if self.color == Config.Pieces.BLACK:
            return (self.row - 1, self.col - 1), (self.row - 1, self.col + 1)
        return (self.row + 1, self.col - 1), (self.row + 1, self.col + 1)

    def jump_rules(self):
        if self.color == Config.Pieces.BLACK:
            return {(self.row - 2, self.col - 2): (self.row - 1, self.col - 1),
                    (self.row - 2, self.col + 2): (self.row - 1, self.col + 1)}
        return {(self.row + 2, self.col - 2): (self.row + 1, self.col - 1),
                (self.row + 2, self.col + 2): (self.row + 1, self.col + 1)}

    def make_king(self):
        self.king = True

    def draw(self, window):
        color = Config.WHITE_PIECES_COLOR if self.color == Config.Pieces.WHITE else Config.BLACK_PIECES_COLOR
        pygame.draw.circle(window, Config.OUTLINE_COLOR, (self.x, self.y), Config.PIECE_RADIUS + Config.PIECE_OUTLINE)
        pygame.draw.circle(window, color, (self.x, self.y), Config.PIECE_RADIUS)

    def move(self, row, col):
        self.row = row
        self.col = col
        self.calc_pos()