import pygame

from gomoku.envs.board import Board


size = width, height = 500, 500
black = 0, 0, 0


class GomokuGUI(object):
    def __init__(self):
        self._board = Board()
        pygame.init()
        self._screen = pygame.display.set_mode(size)
        self._running = True

    def on_event(self, event):
        if event.type == pygame.QUIT:
            self._running = False

    def on_execute(self):
        while self._running:
            for event in pygame.event.get():
                self.on_event(event)

            self._screen.fill((255, 255, 255))
            pygame.draw.circle(self._screen, (0, 0, 255), (250, 250), 75)

            pygame.display.flip()
        pygame.quit()


if __name__ == "__main__":
    gomoku = GomokuGUI()
    gomoku.on_execute()
