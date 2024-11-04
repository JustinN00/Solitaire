import pygame


class Card:
    def __init__(self, suit, rank, shown = False):
        self.suit = suit
        self.rank = rank
        self.shown = shown
        self.card_rect = pygame.Rect(10, 10, 10, 10)

    def draw(self, surface):
        if self.shown:
            pygame.draw.rect(surface, "white", self.card_rect)
        else:
            pygame.draw.rect(surface, "red", self.card_rect)

class Board:
    def __init__(self, surface):
        self.surface = surface
        self.deck: list[Card] = []
        self.files = [[] for _ in range(6)]

    def create_deck(self):
        self.deck = []
        for i in range(1,53):
            self.deck.append(Card(i%4, i//13))

    def draw_board(self):
        for card in self.deck:
            card.draw(self.surface)

                

    

    




pygame.init()
screen = pygame.display.set_mode((1200, 720))
game_board = Board(screen)
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