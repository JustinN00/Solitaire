import pygame


class Card:
    def __init__(self, suit, rank, shown = False):
        self.suit = suit
        self.rank = rank
        self.shown = shown
        self.card_width = 35
        self.card_height =50
        self.card_rect = pygame.Rect(10, 10, self.card_width, self.card_height)

    def draw(self, surface: pygame.surface):
        if self.shown:
            pygame.draw.rect(surface, "white", self.card_rect)
        else:
            pygame.draw.rect(surface, "red", self.card_rect)

class Column:
    def __init__(self, x_location, y_location, surface):
        self.x_location = x_location
        self.y_location = y_location
        self.surface = surface
        self.cards: list[Card] = []

    def draw_column(self):
        y_offset = 0
        self.refresh_column()
        for card in self.cards:
            card.card_rect = pygame.Rect(self.x_location, (self.y_location + y_offset), card.card_width, card.card_height)
            card.draw(self.surface)
            y_offset += 25

    def refresh_column(self):
        if self.cards[-1].shown == False:
            self.cards[-1].shown = True

class Board:
    def __init__(self, surface):
        self.surface: pygame.surface = surface
        self.deck: list[Card] = []
        self.columns: list[Column] = []
        self.create_deck()
        self.setup_columns()
        

    def create_deck(self):
        self.deck = []
        for i in range(1,53):
            self.deck.append(Card(i%4, i//13))

    def setup_columns(self):
        board_width = self.surface.get_width()
        border_size = board_width/4
        columns_area = board_width - (border_size * 2)
        column_space = columns_area/8

        for i in range(1, 8):
            self.columns.append(Column(border_size + (column_space * i),25, self.surface))
        
        count = 1
        for column in self.columns:
            cards = self.deck[-count:]
            del self.deck[-count:]
            column.cards += cards
            count += 1

    def draw_board(self):
        self.surface.fill("green")
        for column in self.columns:
            column.draw_column()

