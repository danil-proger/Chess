import pygame
import enum


pygame.display.init()
WIDTH = min(pygame.display.Info().current_w, pygame.display.Info().current_h) * 3 // 4
HEIGHT = min(pygame.display.Info().current_w, pygame.display.Info().current_h) * 3 // 4
ROWS = 8
COLUMNS = 8
NUMBER_OF_PIECES = 12
SQUARE_SIZE = WIDTH // COLUMNS
PIECE_RADIUS = SQUARE_SIZE * 2 // 5
PIECE_OUTLINE = PIECE_RADIUS // 10
VALID_MOVE_MARK_RADIUS = PIECE_RADIUS // 2

WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))

OUTLINE_COLOR = (128, 128, 128)
POSSIBLE_MOVE_COLOR = (128, 128, 128)
WHITE_TILES_COLOR = (190, 190, 190)
BLACK_TILES_COLOR = (65, 65, 65)
WHITE_PIECES_COLOR = (230, 230, 230)
BLACK_PIECES_COLOR = (25, 25, 25)

delta_first = 1
delta_second = 2


class Pieces(enum.Enum):
    WHITE = 'WHITE'
    BLACK = 'BLACK'