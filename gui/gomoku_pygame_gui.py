# Modified from https://codereview.stackexchange.com/questions/174187/gomoku-in-pygame

import pygame
from pygame.locals import (
    HWSURFACE,
    DOUBLEBUF,
    QUIT,
    MOUSEMOTION
)
from gomoku.envs.board import Board


# Define some colors
BLACK = (0, 0, 0)
WHITE = (245, 245, 245)
RED = (133, 42, 44)
YELLOW = (208, 176, 144)
GREEN = (26, 81, 79)

# Define grid globals
grid_size = 25
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
    def __init__(self):
        self._board = Board()
        pygame.init()
        self._screen = pygame.display.set_mode(screen_size, HWSURFACE | DOUBLEBUF)
        pygame.display.set_caption('Gomoku')
        self._running = True

        self._current_stone_pos = None

    def on_event(self, event):
        if event.type == QUIT:
            self._running = False
        elif event.type == MOUSEMOTION:
            x, y = pygame.mouse.get_pos()
            edge_padding = padding - stone_radius
            if edge_padding <= x <= screen_size[0] - edge_padding and \
                    edge_padding <= y <= board_size + padding*2 - edge_padding:
                self._current_stone_pos = (x, y)
            else:
                self._current_stone_pos = None

    def on_render(self):
        self.render_board_background()
        self.render_current_stone()

    def on_execute(self):
        while self._running:
            for event in pygame.event.get():
                self.on_event(event)
            self.on_render()

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

    def render_current_stone(self):
        if self._current_stone_pos is not None:
            x, y = self._current_stone_pos
            # constrain the current stone to the grid crossing
            x = ((x - padding + grid_size // 2) // (grid_size + margin)) * (grid_size + margin) + padding
            y = ((y - padding + grid_size // 2) // (grid_size + margin)) * (grid_size + margin) + padding
            draw_circle_alpha(self._screen, (0, 0, 0, 127), (x, y), stone_radius)
                

if __name__ == "__main__":
    gomoku = GomokuGUI()
    gomoku.on_execute()
