"""Main code for the Solitaire game"""

import pygame
import game_objects

pygame.init()
screen = pygame.display.set_mode((1200, 720))
game_board = game_objects.Board(screen)
cursor = game_objects.Cursor(game_board)
clock = pygame.time.Clock()

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            match (event.key):
                case pygame.K_RIGHT:
                    cursor.move_right()

                case pygame.K_LEFT:
                    cursor.move_left()

                case pygame.K_UP:
                    cursor.move_up()

                case pygame.K_DOWN:
                    cursor.move_down()
 
                case pygame.K_SPACE:
                    cursor.interact()

    game_board.refresh_all()
    game_board.draw_board()
    cursor.draw_cursor()
    if game_board.check_win():
        print("You win")

    pygame.display.flip()
    clock.tick(60)
pygame.quit()
