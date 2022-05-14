import pygame
import src.Config as Config
import src.Game as Game
import sys
import menu.Button as Button
import bot.algorithm as algorithm


FPS = 60
pygame.font.init()


def get_row_col_from_mouse(pos):
    x, y = pos
    row = y // Config.SQUARE_SIZE
    col = x // Config.SQUARE_SIZE
    return row, col


def checkers():
    run = True
    clock = pygame.time.Clock()
    game = Game.Game()
    winner = None

    while run:
        clock.tick(FPS)

        if game.winner() is not None:
            if game.winner() == Config.Pieces.BLACK:
                winner = 'BLACK'
            else:
                winner = 'WHITE'
            run = False

        if game.turn == Config.Pieces.WHITE:
            value, new_board = algorithm.minimax(game.get_board(), 4, Config.Pieces.WHITE, game)
            game.ai_move(new_board)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                row, col = get_row_col_from_mouse(pos)
                game.select(row, col)

        game.update()

    return winner


def checkers_2x2():
    run = True
    clock = pygame.time.Clock()
    game = Game.Game()
    pygame.display.set_caption('Checkers')
    winner = None
    while run:
        clock.tick(FPS)

        if game.winner() is not None:
            if game.winner() == Config.Pieces.BLACK:
                winner = 'BLACK'
            else:
                winner = 'WHITE'
            run = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                row, column = get_row_col_from_mouse(pos)
                game.select(row, column)

        game.update()
    return winner


def menu():
    last_game_winner = 'UNDEFINED'
    while True:
        screen = pygame.display.set_mode((Config.WIDTH, Config.HEIGHT))
        pygame.display.set_caption('Menu')
        screen.blit(
            pygame.transform.scale(pygame.image.load('src/images/Background.png'), (Config.WIDTH, Config.HEIGHT)),
            (0, 0))

        MENU_MOUSE_POS = pygame.mouse.get_pos()

        MENU_TEXT = pygame.font.Font("src/fonts/font.ttf", 85).render("MAIN MENU", True, "#b68f40")
        MENU_RECT = MENU_TEXT.get_rect(center=(Config.WIDTH // 2, Config.HEIGHT * 1.5 // 10))
        PLAY_BOT_BUTTON = Button.Button(None,
                                        pos=(Config.WIDTH // 2, Config.HEIGHT * 3.5 // 10),
                                        text_input="PLAY VS AI", font=pygame.font.Font("src/fonts/font.ttf", 45),
                                        base_color="#d7fcd4",
                                        hovering_color="White")
        PLAY_BUTTON = Button.Button(None,
                                    pos=(Config.WIDTH // 2, Config.HEIGHT * 5 // 10),
                                    text_input="PLAY WITH FRIEND", font=pygame.font.Font("src/fonts/font.ttf", 45),
                                    base_color="#d7fcd4",
                                    hovering_color="White")
        QUIT_BUTTON = Button.Button(None,
                                    pos=(Config.WIDTH // 2, Config.HEIGHT * 6.5 // 10),
                                    text_input="QUIT", font=pygame.font.Font("src/fonts/font.ttf", 45),
                                    base_color="#d7fcd4",
                                    hovering_color="White")

        LAST_GAME_WINNER_PATTERN = pygame.font.Font("src/fonts/font.ttf", 25).render("THE WINNER OF THE LAST GAME IS",
                                                                                     True, "#b68f40")
        LAST_GAME_WINNER_PATTERN_RECT = LAST_GAME_WINNER_PATTERN.get_rect(
            center=(Config.WIDTH // 2, Config.HEIGHT * 8 // 10))
        LAST_GAME_WINNER = pygame.font.Font("src/fonts/font.ttf", 25).render(last_game_winner, True, "#b68f40")
        LAST_GAME_WINNER_RECT = LAST_GAME_WINNER.get_rect(center=(Config.WIDTH // 2, Config.HEIGHT * 9 // 10))

        screen.blit(MENU_TEXT, MENU_RECT)
        screen.blit(LAST_GAME_WINNER_PATTERN, LAST_GAME_WINNER_PATTERN_RECT)
        screen.blit(LAST_GAME_WINNER, LAST_GAME_WINNER_RECT)

        for button in [PLAY_BOT_BUTTON, PLAY_BUTTON, QUIT_BUTTON]:
            button.change_color(MENU_MOUSE_POS)
            button.update(screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if PLAY_BOT_BUTTON.check_for_input(MENU_MOUSE_POS):
                    last_game_winner = checkers()
                if PLAY_BUTTON.check_for_input(MENU_MOUSE_POS):
                    last_game_winner = checkers_2x2()
                if QUIT_BUTTON.check_for_input(MENU_MOUSE_POS):
                    pygame.quit()
                    sys.exit()

        pygame.display.update()


menu()