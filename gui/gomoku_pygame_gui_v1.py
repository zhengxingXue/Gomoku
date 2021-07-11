import pygame
from pygame.locals import (
    HWSURFACE,
    DOUBLEBUF,
    QUIT,
    MOUSEMOTION,
    MOUSEBUTTONUP
)
from pygame_widgets import Button
from gui.resources.pygame_DropDown import DropDown
from gomoku.envs.board import Board
from gomoku.envs.boardUtils import StoneColor
from gomoku.envs.opponent import EasyAgent, RandomAgent


# Define drawing constants
BLACK = (0, 0, 0)
YELLOW = (208, 176, 144)
WHITE = (255, 255, 255)
BUTTON_INACTIVE = (236, 233, 226)

GRID_SIZE = 20
MARGIN = 1
STONE_RADIUS = GRID_SIZE // 2 - MARGIN
BOARD_SIZE = (GRID_SIZE + MARGIN) * 14 + MARGIN

TOP_SPACING = 80
BOTTOM_SPACING = 80
PADDING = 20
SCREEN_WIDTH = BOARD_SIZE + PADDING * 2
SCREEN_HEIGHT = SCREEN_WIDTH + TOP_SPACING + BOTTOM_SPACING
SCREEN_SIZE = SCREEN_WIDTH, SCREEN_HEIGHT


# helper function
def draw_circle_alpha(surface, color, center, radius):
    target_rect = pygame.Rect(center, (0, 0)).inflate((radius * 2, radius * 2))
    shape_surf = pygame.Surface(target_rect.size, pygame.SRCALPHA)
    pygame.draw.circle(shape_surf, color, (radius, radius), radius)
    surface.blit(shape_surf, target_rect)


class DropDownButton(DropDown):
    def __init__(self, surf, color_menu, color_option, x, y, w, h, font, main, options, onChange):
        DropDown.__init__(self, color_menu, color_option, x, y, w, h, font, main, options)
        self.surf = surf
        self.onChange = onChange

    def draw(self, surf=None, border_radius=5):
        DropDown.draw(self, self.surf, border_radius)

    def listen(self, events):
        selected_option = DropDown.update(self, events)
        if selected_option >= 0:
            if self.main != self.options[selected_option]:
                self.main = self.options[selected_option]
                self.onChange()
            else:
                self.main = self.options[selected_option]


class GomokuGUI(object):
    def __init__(self):
        pygame.init()
        self._screen = pygame.display.set_mode(SCREEN_SIZE, HWSURFACE | DOUBLEBUF)
        pygame.display.set_caption('Gomoku')
        self._set_up_buttons()
        self._running = True
        self._board = Board(board_size=15)
        self._current_stone_pos = None
        self._opponent = None
        self._round_reset()

    def _round_reset(self):
        self._opponent_win_time = 0
        self._player_win_time = 0
        self._board_reset()

    def _board_reset(self):
        self._board.reset()
        self._have_five = False
        self._is_full = False

    def on_execute(self):
        while self._running:
            events = pygame.event.get()
            for event in events:
                self.on_event(event)
            self.on_render()
            self._buttons_listen_and_draw(events)
            pygame.display.flip()
        pygame.quit()

    def on_event(self, event):
        if event.type == QUIT:
            self._running = False
        elif event.type == MOUSEMOTION and not self._game_mode_button.draw_menu:
            self._update_current_stone_pos()
        elif event.type == MOUSEBUTTONUP and not self._game_mode_button.draw_menu:
            self._update_current_stone_pos()
            if self._current_stone_pos is not None and not self.board_is_done:
                row, col = self.current_stone_coordinate_on_grid
                col = self._col_converter(col)
                if self._board.board_state[row][col] == 0:
                    self._have_five, self._is_full = self._board.step([row, col])
                    if self._have_five:
                        if self._board.current_stone_color == StoneColor.black:
                            self._player_win_time += 1
                        else:
                            self._opponent_win_time += 1
                    if self._opponent is not None and not self.board_is_done:
                        opponent_action, _ = self._opponent.predict(obs=None)
                        self._have_five, self._is_full = self._board.step(opponent_action)
                        self._opponent_win_time += 1 if self._have_five else 0

            # game is done, click anywhere inside the board will reset the board
            elif self._current_stone_pos is not None and self.board_is_done:
                self._board_reset()

    def _update_current_stone_pos(self):
        x, y = pygame.mouse.get_pos()
        edge_padding = PADDING - STONE_RADIUS
        if edge_padding <= x <= SCREEN_WIDTH - edge_padding and \
                edge_padding + TOP_SPACING <= y <= TOP_SPACING + BOARD_SIZE + PADDING * 2 - edge_padding:
            self._current_stone_pos = (x, y-TOP_SPACING)
        else:
            self._current_stone_pos = None

    def on_render(self):
        self.render_board_background()
        self.render_round_info()
        self.render_game_info()
        self.render_placed_stones()
        self.render_current_stone()

    def render_board_background(self):
        self._screen.fill(YELLOW)
        # Draw background rect for game area
        pygame.draw.rect(self._screen, BLACK, [PADDING, PADDING+TOP_SPACING, BOARD_SIZE, BOARD_SIZE])
        # Draw the grid
        for row in range(14):
            for column in range(14):
                pygame.draw.rect(self._screen, YELLOW,
                                 [(MARGIN + GRID_SIZE) * column + MARGIN + PADDING,
                                  (MARGIN + GRID_SIZE) * row + MARGIN + PADDING + TOP_SPACING,
                                  GRID_SIZE,
                                  GRID_SIZE])

    def render_round_info(self):
        info = str(self._opponent_win_time) + " : " + str(self._player_win_time)
        font = pygame.font.Font(pygame.font.get_default_font(), 18)
        text = font.render(info, True, BLACK)
        textRect = text.get_rect()
        textRect.centerx = SCREEN_WIDTH // 2
        textRect.centery = (TOP_SPACING + PADDING) // 2
        self._screen.blit(text, textRect)

    def render_game_info(self):
        left_stone_center = PADDING + 50, (TOP_SPACING + PADDING) * 4 / 5
        self._render_stone_helper(WHITE, left_stone_center)
        right_stone_center = SCREEN_WIDTH - PADDING - 50, (TOP_SPACING + PADDING) * 4 / 5
        self._render_stone_helper(BLACK, right_stone_center)

    def render_placed_stones(self):
        for stone in self._board.stone_array:
            row, col = stone.position
            col = self._col_converter(col)
            def helper(a): return (MARGIN + GRID_SIZE) * a + PADDING
            center = (helper(row), helper(col)+TOP_SPACING)
            color = BLACK if stone.color == StoneColor.black else WHITE
            self._render_stone_helper(color, center)

    def _render_stone_helper(self, color, center):
        pygame.draw.circle(self._screen, color, center, STONE_RADIUS, 0)
        pygame.draw.circle(self._screen, BLACK, center, STONE_RADIUS, 1)

    def render_current_stone(self):
        if self._current_stone_pos is not None and not self.board_is_done:
            row, col = self.current_stone_coordinate_on_grid
            col_in_board = self._col_converter(col)
            if self._board.board_state[row][col_in_board] == 0:
                # constrain the current stone to the grid crossing
                def helper(a): return a * (GRID_SIZE + MARGIN) + PADDING
                color = (0, 0, 0, 63) if self._board.current_stone_color == StoneColor.black \
                    else (255, 255, 255, 127)
                draw_circle_alpha(self._screen, color, (helper(row), helper(col) + TOP_SPACING), STONE_RADIUS)

    def _col_converter(self, col):
        # convert bottom left corner origin to top left
        return self._board.board_size - 1 - col

    def _set_up_buttons(self):
        self._buttons = []
        self._set_up_restart_button()
        self._set_up_reset_round_button()
        self._set_up_player_button()
        self._set_up_game_mode_selection_drop_down_button()

    def _buttons_listen_and_draw(self, events):
        for button in self._buttons:
            button.listen(events)
            button.draw()

    def _set_up_restart_button(self):
        width, height = 60, 30
        x = PADDING + BOARD_SIZE - width
        y = SCREEN_HEIGHT - (BOTTOM_SPACING + height + PADDING) // 2

        def onClick():
            self._board_reset()

        restart_button = Button(
            self._screen, x, y, width, height, text='Restart',
            inactiveColour=BUTTON_INACTIVE, hoverColour=WHITE,
            radius=5, onClick=onClick
        )
        self._buttons.append(restart_button)

    def _set_up_reset_round_button(self):
        width, height = 60, 30
        x = PADDING
        y = SCREEN_HEIGHT - (BOTTOM_SPACING + height + PADDING) // 2

        def onClick():
            self._round_reset()

        reset_round_button = Button(
            self._screen, x, y, width, height, text='Reset',
            inactiveColour=BUTTON_INACTIVE, hoverColour=WHITE,
            radius=5, onClick=onClick
        )
        self._buttons.append(reset_round_button)

    def _set_up_game_mode_selection_drop_down_button(self):
        width, height = 100, 30
        x = PADDING
        y = (TOP_SPACING+PADDING) // 2 - height // 2

        def onChange():
            if self.game_mode == "Random Agent":
                self._opponent = RandomAgent(self._board, StoneColor.white)
            elif self.game_mode == "Easy Agent":
                self._opponent = EasyAgent(self._board, StoneColor.white)
            else:
                self._opponent = None
            self._round_reset()

        COLOR_INACTIVE = BUTTON_INACTIVE
        COLOR_ACTIVE = WHITE
        COLOR_LIST_INACTIVE = BUTTON_INACTIVE
        COLOR_LIST_ACTIVE = WHITE
        game_mode_button = DropDownButton(
            self._screen,
            [COLOR_INACTIVE, COLOR_ACTIVE],
            [COLOR_LIST_INACTIVE, COLOR_LIST_ACTIVE],
            x, y, width, height,
            pygame.font.SysFont(None, 20),
            "Opponent", ["Player", "Random Agent", "Easy Agent"],
            onChange
        )
        self._buttons.append(game_mode_button)
        self._game_mode_button = game_mode_button

    def _set_up_player_button(self):
        width, height = 100, 30
        x = PADDING + BOARD_SIZE - width
        y = (TOP_SPACING + PADDING) // 2 - height // 2

        def onClick():
            pass

        player_button = Button(
            self._screen, x, y, width, height, text='Player',
            inactiveColour=BUTTON_INACTIVE, hoverColour=WHITE,
            radius=5, onClick=onClick
        )
        self._buttons.append(player_button)

    @property
    def game_mode(self):
        return self._game_mode_button.main

    @property
    def current_stone_coordinate_on_grid(self):
        """
        :return: stone coordinate on grid, top left corner as origin
        """
        x, y = self._current_stone_pos
        def helper(a): return (a - PADDING // 2) // (GRID_SIZE + MARGIN)
        return helper(x), helper(y)

    @property
    def board_is_done(self):
        return self._have_five or self._is_full


if __name__ == "__main__":
    gomoku = GomokuGUI()
    gomoku.on_execute()
