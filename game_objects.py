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
        self.refresh()
        pygame.draw.rect(self.surface, "yellow", self.empty_rect)
        for card in self.cards:
            card.draw(self.surface)

    def refresh(self) -> None:
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



class Cell:
    def __init__(self, x_location, y_location, surface: pygame.Surface):
        self.x_location = x_location
        self.y_location = y_location
        self.surface = surface
        self.cards: list[Card] = []
        self.cell_rect = pygame.rect.Rect(x_location, y_location, 35, 50)

    def refresh(self):
        for card in self.cards:
            card.card_rect = pygame.Rect(
                self.x_location,
                self.y_location,
                card.card_width,
                card.card_height,
            )

    def draw_cell(self):
        pygame.draw.rect(self.surface, "yellow", self.cell_rect)
        self.draw_cards()

    def draw_cards(self): 
        for card in self.cards:
            card.draw(self.surface)


class Deck(Cell):
    def get_cards(self):
        if self.cards:
            return self.cards.pop()



class DrawPile(Cell):
    pass


class Foundation(Cell):
    def __init__(self, suit, x_location, y_location, surface):
        super().__init__(x_location, y_location, surface)
        self.suit = suit


class Board:
    def __init__(self, surface: pygame.Surface):
        self.surface: pygame.Surface = surface
        self.deck: list[Card] = []
        self.columns: list[Column] = []
        self.top_row: list[Cell | Deck] = []
        self.cells = []
        self.create_deck()
        self.setup_columns()
        self.create_top_row()

    def create_deck(self) -> None:
        for i in range(1, 53):
            self.deck.append(Card(rank=(i % 13) + 1, suit=(i // 4) + 1))

    def create_top_row(self) -> None:
        self.cells.append(Deck(self.border_size + (self.column_space * 1), 10, self.surface))
        self.cells.append(DrawPile(self.border_size + (self.column_space * 2), 10, self.surface))
        for i in range(1,5):
            self.cells.append(Foundation(i, self.border_size + (self.column_space * (i + 3)), 10, self.surface))

        self.cells[0].cards = self.deck
        self.cells[0].refresh()


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
            column.refresh()


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
        self.current_upper_column = 0
        self.cursor_rect = pygame.rect.Rect(1, 1, 1, 1)
        self.selection: Card | None = None
        self.selection_column: int | None = None
        self.selection_column_upper = None
        self.cursor_height: int = -1
        self.upper = False
        self.update_column()

    def draw_cursor(self) -> None:
        pygame.draw.rect(self.board.surface, "black", self.cursor_rect)

    def update_column(self) -> None:
        if self.upper:
            if self.board.cells[self.current_upper_column].cards:
                self.cursor_rect = pygame.rect.Rect(
                    self.board.cells[self.current_upper_column].cards[self.cursor_height].card_rect.left,
                    self.board.cells[self.current_upper_column].cards[self.cursor_height].card_rect.top,
                    5,
                    5,
                )
            else:
                self.cursor_rect = pygame.rect.Rect(
                    self.board.cells[self.current_upper_column].cell_rect.left,
                    self.board.cells[self.current_upper_column].cell_rect.top,
                    5,
                    5,
                )
                
        
        elif self.board.columns[self.current_column].cards:
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
        if self.upper:
            self.current_upper_column += 1
            self.cursor_height = -1
            if self.current_upper_column > len(self.board.cells) -1:
                self.current_upper_column = 0
        else:
            self.current_column += 1
            self.cursor_height = -1
            if self.current_column > len(self.board.columns) - 1:
                self.current_column = 0
        self.update_column()

    def move_left(self) -> None:
        if self.upper:
            self.current_upper_column -= 1
            self.cursor_height = -1
            if self.current_upper_column < 0:
                self.current_upper_column = len(self.board.cells) - 1
        else:
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
        elif not self.upper:
            self.upper = True
        elif self.upper:
            self.upper = False
        self.update_column()

    def interact(self) -> None:
        def move_cards(self):
            if self.selection_column is not None:
                column = self.board.columns[self.selection_column]
            else:
                column = self.board.cells[self.selection_column_upper]
            for i in self.selection:
                for i in range(len(self.selection)):
                    column.cards.pop()
                if self.upper:
                    self.board.cells[self.current_upper_column].cards += self.selection
                else:
                    self.board.columns[self.current_column].cards += self.selection
                for i in self.selection:
                    i.selected=False
                self.selection = None
                if self.upper:
                    self.board.cells[self.current_upper_column].refresh()
                else:
                    self.board.columns[self.current_column].refresh()
            self.update_column()
            self.selection_column = None
            self.selection_column_upper = None

        if self.upper:
            cell = self.board.cells[self.current_upper_column]
            #Interacting with Deck
            if isinstance(cell, Deck):
                if cell.cards:
                    flipped_card = cell.get_cards()
                    flipped_card.shown = True
                    self.board.cells[1].cards.append(flipped_card)
                else:
                    if self.board.cells[1].cards:
                        for i in self.board.cells[1].cards:
                            i.shown = False
                        cell.cards += self.board.cells[1].cards
                        cell.cards.reverse()
                        self.board.cells[1].cards = []
                if self.selection:
                    for i in self.selection:
                        i.selected=False
                self.selection = None
                self.selection_column = None
                self.selection_column_upper = None
                cell.refresh()
                self.board.cells[1].refresh()
                return
            
            #Interacting with DrawPile
            if isinstance(cell, DrawPile):
                if self.selection:
                    for i in self.selection:
                        i.selected=False
                self.selection = None
                self.selection_column = None
                self.selection_column_upper = None
                if cell.cards:
                    self.selection = cell.cards[-1:]
                    self.selection_column_upper = self.current_upper_column
                    for i in self.selection:
                        i.selected = True

            elif not self.selection and cell.cards:
                if isinstance(cell, Foundation):
                    self.selection = cell.cards[-1:]
                    self.selection_column_upper = self.current_upper_column
                    for i in self.selection:
                        i.selected = True
            elif self.selection:
                if self.validate_move():
                    move_cards(self)
        elif not self.selection and self.board.columns[self.current_column].cards:
            if self.validate_select():
                self.selection = self.board.columns[self.current_column].cards[self.cursor_height:]
                self.selection_column = self.current_column
                for i in self.selection:
                    i.selected = True
        elif self.selection and (self.selection_column is not None or self.selection_column_upper is not None):
            if self.validate_move():
                move_cards(self)
        

    def validate_move(self) -> None:
        #TODO
        return True

    def validate_select(self) -> None:
        #TODO
        return True
