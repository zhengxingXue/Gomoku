# Modified from https://codereview.stackexchange.com/questions/174187/gomoku-in-pygame

import pygame
from pygame.locals import (
    HWSURFACE,
    DOUBLEBUF,
    QUIT,
    MOUSEMOTION,
    MOUSEBUTTONUP
)
from pygame_widgets import Button
from gomoku.envs.board import Board
from gomoku.envs.boardUtils import StoneColor
from gomoku.envs.gomoku_env import GomokuEnv

# Define some colors
BLACK = (0, 0, 0)
WHITE = (245, 245, 245)
RED = (133, 42, 44)
YELLOW = (208, 176, 144)
GREEN = (26, 81, 79)

# Define grid globals
grid_size = 26
margin = 1
padding = 20
stone_radius = grid_size // 2 - margin
board_size = (grid_size + margin) * 14 + margin
screen_size = board_size + padding * 2, board_size + padding * 2 + 100


# helper function
def draw_circle_alpha(surface, color, center, radius):
    target_rect = pygame.Rect(center, (0, 0)).inflate((radius * 2, radius * 2))
    shape_surf = pygame.Surface(target_rect.size, pygame.SRCALPHA)
    pygame.draw.circle(shape_surf, color, (radius, radius), radius)
    surface.blit(shape_surf, target_rect)


class GomokuGUI(object):
    USE_ENV = False

    def __init__(self):
        if self.USE_ENV:
            self._env = GomokuEnv()
            self._board = self._env.board
        else:
            self._board = Board()
            # self._board.step([0, 0])

        pygame.init()
        self._screen = pygame.display.set_mode(screen_size, HWSURFACE | DOUBLEBUF)
        pygame.display.set_caption('Gomoku')

        self._set_up_buttons()

        self._running = True

        if self.USE_ENV:
            self._done = False
        else:
            self._have_five = False
            self._is_full = False

        self._current_stone_pos = None

    def _set_up_buttons(self):
        self._buttons = []
        self._set_up_reset_button()

    def _set_up_reset_button(self):
        width, height = 60, 30
        x = self._screen.get_width() // 2 - width // 2
        y = self._screen.get_width() + 20

        def onClick():
            if self.USE_ENV:
                self._env.reset()
            else:
                self._board.reset()

        reset_button = Button(
            self._screen, x, y, width, height, text='Reset',
            inactiveColour=(236, 233, 226), hoverColour=WHITE,
            radius=5, onClick=onClick
        )
        self._buttons.append(reset_button)

    def _buttons_listen_and_draw(self, events):
        for button in self._buttons:
            button.listen(events)
            button.draw()

    def _update_current_stone_pos(self):
        x, y = pygame.mouse.get_pos()
        edge_padding = padding - stone_radius
        if edge_padding <= x <= screen_size[0] - edge_padding and \
                edge_padding <= y <= board_size + padding * 2 - edge_padding:
            self._current_stone_pos = (x, y)
        else:
            self._current_stone_pos = None

    def _col_converter(self, col):
        # convert bottom left corner origin to top left
        return self._board.board_size - 1 - col

    def on_event(self, event):
        if event.type == QUIT:
            self._running = False

        elif event.type == MOUSEMOTION:
            self._update_current_stone_pos()

        elif event.type == MOUSEBUTTONUP:
            self._update_current_stone_pos()
            if self._current_stone_pos is not None:
                row, col = self.current_stone_coordinate_on_grid
                col = self._col_converter(col)
                if self._board.board_state[row][col] == 0:
                    if self.USE_ENV:
                        _, _, self._done, _ = self._env.step([row, col])
                    else:
                        self._have_five, self._is_full = self._board.step([row, col])

    def on_render(self):
        self.render_board_background()
        self.render_placed_stones()
        self.render_current_stone()

    def on_execute(self):
        while self._running:
            events = pygame.event.get()
            for event in events:
                self.on_event(event)
            self.on_render()
            self._buttons_listen_and_draw(events)
            pygame.display.flip()
        pygame.quit()

    def render_board_background(self):
        self._screen.fill(YELLOW)
        # Draw background rect for game area
        pygame.draw.rect(self._screen, BLACK, [padding, padding, board_size, board_size])

        # Draw the grid
        for row in range(14):
            for column in range(14):
                pygame.draw.rect(self._screen, YELLOW,
                                 [(margin + grid_size) * column + margin + padding,
                                  (margin + grid_size) * row + margin + padding,
                                  grid_size,
                                  grid_size])

    def render_placed_stones(self):
        for stone in self._board.stone_array:
            row, col = stone.position
            col = self._col_converter(col)

            def helper(a): return (margin + grid_size) * a + padding

            center = (helper(row), helper(col))
            color = BLACK if stone.color == StoneColor.black else WHITE
            pygame.draw.circle(self._screen, color, center, stone_radius, 0)
            pygame.draw.circle(self._screen, BLACK, center, stone_radius, 1)

    def render_current_stone(self):
        if self._current_stone_pos is not None:
            row, col = self.current_stone_coordinate_on_grid
            col_in_board = self._col_converter(col)
            if self._board.board_state[row][col_in_board] == 0:
                # constrain the current stone to the grid crossing
                def helper(a): return a * (grid_size + margin) + padding

                color = (0, 0, 0, 63) if self._board.current_stone_color == StoneColor.black \
                    else (255, 255, 255, 127)
                draw_circle_alpha(self._screen, color, (helper(row), helper(col)), stone_radius)

    @property
    def current_stone_coordinate_on_grid(self):
        """
        :return: stone coordinate on grid, top left corner as origin
        """
        x, y = self._current_stone_pos

        def helper(a): return (a - padding + grid_size // 2) // (grid_size + margin)

        return helper(x), helper(y)


if __name__ == "__main__":
    gomoku = GomokuGUI()
    gomoku.on_execute()
