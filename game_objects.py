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
        x1 = 10
        y1 = 10
        width = 10
        height = 15

        for card in self.deck:
            card.card_rect = pygame.Rect(x1, y1, width, height)
            card.draw(self.surface)
            x1 += 20
