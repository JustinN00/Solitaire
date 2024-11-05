"""Game Objects for the Solitaire game"""

import pygame

pygame.init()
my_font = pygame.font.Font(None, 36)

rank_icon_dict = {
    1: "A",
    11: "J",
    12: "Q",
    13: "K",
}


class Card:
    """class for a card"""

    def __init__(self, suit: int, rank: int, shown: bool = False):
        self.suit = suit
        self.rank = rank
        self.shown = shown
        self.card_width = 35
        self.card_height = 50
        self.selected = False
        self.card_rect = pygame.Rect(10, 10, self.card_width, self.card_height)
        self.set_icons()
        if self.suit % 2 == 0:
            self.color = "black"
        else:
            self.color = "red"

    def draw(self, surface: pygame.Surface) -> None:
        # TODO move out of draw method
        border_rect = pygame.rect.Rect(
            self.card_rect.left,
            self.card_rect.top,
            self.card_rect.width,
            self.card_rect.height,
        )
        border_rect.left -= 1
        border_rect.top -= 1
        border_rect.width += 2
        border_rect.height += 2
        if self.selected:
            border_color = "yellow"
        else:
            border_color = "black"
        pygame.draw.rect(surface, border_color, border_rect)
        if self.shown:
            pygame.draw.rect(surface, "white", self.card_rect)
            text = my_font.render(str(self.rank_icon), True, self.color)
            surface.blit(text, (self.card_rect.x, self.card_rect.y))
        else:
            pygame.draw.rect(surface, "red", self.card_rect)

    def set_icons(self) -> None:
        if self.rank in [1, 11, 12, 13]:
            self.rank_icon = rank_icon_dict[self.rank]
        else:
            self.rank_icon = str(self.rank)


class Column:
    def __init__(self, x_location: int, y_location: int, surface: pygame.Surface):
        self.x_location = x_location
        self.y_location = y_location
        self.surface = surface
        self.cards: list[Card] = []
        self.empty_rect = pygame.rect.Rect(x_location, y_location, 35, 50)

    def draw_column(self) -> None:
        self.refresh_column()
        pygame.draw.rect(self.surface, "yellow", self.empty_rect)
        for card in self.cards:
            card.draw(self.surface)

    def refresh_column(self) -> None:
        y_offset = 0
        for card in self.cards:
            card.card_rect = pygame.Rect(
                self.x_location,
                (self.y_location + y_offset),
                card.card_width,
                card.card_height,
            )
            y_offset += 15
        if self.cards:
            if self.cards[-1].shown == False:
                self.cards[-1].shown = True


class Deck:
    def __init__(self):
        self.cards = []

class Cell:
    def __init__(self, suit: int, x_location, y_location, surface: pygame.Surface):
        self.suit = suit
        self.x_location = x_location
        self.y_location = y_location
        self.surface = surface
        self.cards = []
        self.cell_rect = pygame.rect.Rect(x_location, y_location, 35, 50)

    def draw_cell(self):
        pygame.draw.rect(self.surface, "yellow", self.cell_rect)


class Board:
    def __init__(self, surface: pygame.Surface):
        self.surface: pygame.Surface = surface
        self.deck: list[Card] = []
        self.columns: list[Column] = []
        self.cells: list[Cell] = []
        self.create_deck()
        self.setup_columns()
        self.create_cells()

    def create_deck(self) -> None:
        self.deck = []
        for i in range(1, 53):
            self.deck.append(Card(rank=(i % 13) + 1, suit=(i // 4) + 1))

    def create_cells(self) -> None:
        for i in range(1,5):
            self.cells.append(Cell(i, self.border_size + (self.column_space * (i + 3)), 10, self.surface))

    def setup_columns(self) -> None:
        board_width = self.surface.get_width()
        board_height = self.surface.get_height()
        y_value = board_height/6
        self.border_size = board_width / 4
        columns_area = board_width - (self.border_size * 2)
        self.column_space = columns_area / 8

        for i in range(1, 8):
            self.columns.append(
                Column(int(self.border_size + (self.column_space * i)), y_value, self.surface)
            )

        count = 1
        for column in self.columns:
            cards = self.deck[-count:]
            del self.deck[-count:]
            column.cards += cards
            count += 1
            column.refresh_column()

    def draw_board(self) -> None:
        self.surface.fill("green")
        for column in self.columns:
            column.draw_column()
        for cell in self.cells:
            cell.draw_cell()


class Cursor:
    def __init__(self, board: Board) -> None:
        self.board = board
        self.current_column = 0
        self.cursor_rect = pygame.rect.Rect(1, 1, 1, 1)
        self.selection: Card | None = None
        self.selection_column: int | None = None
        self.cursor_height: int = -1
        self.update_column()

    def draw_cursor(self) -> None:
        pygame.draw.rect(self.board.surface, "black", self.cursor_rect)

    def update_column(self) -> None:
        if self.board.columns[self.current_column].cards:
            self.cursor_rect = pygame.rect.Rect(
                self.board.columns[self.current_column].cards[self.cursor_height].card_rect.left,
                self.board.columns[self.current_column].cards[self.cursor_height].card_rect.top,
                5,
                5,
            )
        else:
            self.cursor_rect = pygame.rect.Rect(
                self.board.columns[self.current_column].empty_rect.left,
                self.board.columns[self.current_column].empty_rect.top,
                5,
                5,
            )

    def move_right(self) -> None:
        self.current_column += 1
        self.cursor_height = -1
        if self.current_column > len(self.board.columns) - 1:
            self.current_column = 0
        self.update_column()

    def move_left(self) -> None:
        self.current_column -= 1
        self.cursor_height = -1
        if self.current_column < 0:
            self.current_column = len(self.board.columns) - 1
        self.update_column()

    def move_up(self) -> None:
        if abs(self.cursor_height - 1) <= len(self.board.columns[self.current_column].cards) \
        and self.board.columns[self.current_column].cards[self.cursor_height -1].shown == True:
            self.cursor_height -= 1
            self.update_column()

    def move_down(self) -> None:
        if (self.cursor_height + 1) <= -1:
            self.cursor_height += 1
            self.update_column()

    def interact(self) -> None:
        if not self.selection and self.board.columns[self.current_column].cards:
            if self.validate_select():
                self.selection = self.board.columns[self.current_column].cards[self.cursor_height:]
                self.selection_column = self.current_column
                for i in self.selection:
                    i.selected = True
        elif self.selection and self.selection_column is not None:
            if self.validate_move():
                for i in range(len(self.selection)):
                    self.board.columns[self.selection_column].cards.pop()
                self.board.columns[self.current_column].cards += self.selection
                for i in self.selection:
                    i.selected = False
                self.selection = None
                self.board.columns[self.current_column].refresh_column()
                self.update_column()
        

    def validate_move(self) -> None:
        #TODO
        return True

    def validate_select(self) -> None:
        #TODO
        return True
