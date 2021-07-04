import random


class Agent(object):
    def __init__(self, board, stone_color):
        self._board = board
        self.stone_color = stone_color

    @property
    def board(self):
        return self._board


class RandomAgent(Agent):
    def __init__(self, board, stone_color):
        Agent.__init__(self, board, stone_color)

    def predict(self, obs=None):
        not_found = True
        # Optimize
        while not_found:
            row = self._random_rc()
            col = self._random_rc()
            not_found = self._board.board_state[row][col] != 0
        return [row, col], None

    def _random_rc(self):
        return random.randint(0, self._board.board_size - 1)