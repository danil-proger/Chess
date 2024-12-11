import pygame
import src.Config as Config
import src.Checker as Checker


class King(Checker.Checker):
    crown_image = pygame.transform.scale(pygame.image.load('src/images/Crown.png'), (50, 50))

    def move_rules(self):
        return (self.row + Config.delta_first, self.col - Config.delta_first), (self.row + Config.delta_first, self.col + Config.delta_first), (self.row - Config.delta_first, self.col - Config.delta_first), (
            self.row - Config.delta_first, self.col + Config.delta_first)

    def jump_rules(self):
        return {(self.row + Config.delta_second, self.col - Config.delta_second): (self.row + Config.delta_first, self.col - Config.delta_first),
                (self.row + Config.delta_second, self.col + Config.delta_second): (self.row + Config.delta_first, self.col + Config.delta_first),
                (self.row - Config.delta_second, self.col - Config.delta_second): (self.row - Config.delta_first, self.col - Config.delta_first),
                (self.row - Config.delta_second, self.col + Config.delta_second): (self.row - Config.delta_first, self.col + Config.delta_first)}

    def draw(self, window):
        color = Config.WHITE_PIECES_COLOR if self.color == Config.Pieces.WHITE else Config.BLACK_PIECES_COLOR
        pygame.draw.circle(window, Config.OUTLINE_COLOR, (self.x, self.y), Config.PIECE_RADIUS + Config.PIECE_OUTLINE)
        pygame.draw.circle(window, color, (self.x, self.y), Config.PIECE_RADIUS)
        window.blit(self.crown_image,
                    (self.x - self.crown_image.get_width() // Config.delta_second, self.y - self.crown_image.get_height() // Config.delta_second))