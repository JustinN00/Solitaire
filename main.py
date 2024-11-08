"""Main code for the Solitaire game"""

import pygame
import game_objects

pygame.init()
my_font = pygame.font.Font(None, 36)
screen = pygame.display.set_mode((1200, 720))
game_board = game_objects.Board(screen)
cursor = game_objects.Cursor(game_board)
clock = pygame.time.Clock()
win_screen_rect = pygame.rect.Rect(screen.get_width() / 3, screen.get_height()/3, screen.get_width() / 3, screen.get_height()/3)
win_text = my_font.render("You are the Master of Solitaire™", True, "black")
esc_text = my_font.render("ESC: Quit", True, "black")
arrow_text = my_font.render("Arrows: Move", True, "black")
space_text = my_font.render("Space: Select", True, "black")

won = False
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if not won:
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
            if won:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        pass

            if event.key == pygame.K_ESCAPE:
                running = False

    game_board.refresh_all()
    game_board.draw_board()
    cursor.draw_cursor()
    if game_board.check_win():
        won = True

    if won:
        pygame.draw.rect(screen, "red", win_screen_rect)
        screen.blit(win_text, (win_screen_rect.x + 10, win_screen_rect.centery - 20))

    screen.blit(esc_text, (1,1))
    screen.blit(arrow_text, (1, 30))
    screen.blit(space_text, (1, 59))


    pygame.display.flip()
    clock.tick(60)
pygame.quit()
