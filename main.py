import pygame
import game_objects

pygame.init()
screen = pygame.display.set_mode((1200, 720))
game_board = game_objects.Board(screen)
game_board.create_deck()


clock = pygame.time.Clock()


running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running - False
                                  
    screen.fill("green")
    game_board.draw_board()

    pygame.display.flip()
    clock.tick(60)
pygame.quit()