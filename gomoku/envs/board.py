import matplotlib.pyplot as plt
import numpy as np
from gomoku.envs.boardUtils import BoardPattern, Stone, StoneColor


class BoardPositionAlreadyTaken(Exception):
    pass


class Board(object):
    def __init__(self, board_size=15):
        self._board_size = board_size
        self.reset()

    def reset(self):
        """
        reset the board
        """
        self._current_stone_color = StoneColor.black
        self._current_step = 0
        self._board_state = np.zeros((self._board_size, self._board_size), dtype=int)
        self._board_stone = [[0] * self._board_size for _ in range(self._board_size)]
        self._stone_array = []
        self._board_patterns = BoardPattern(self)

    def step(self, action):
        """
        :param action: [row, column]
        :return: (have_five, is_full)
        """
        row, col = action

        if self._board_state[row][col] != 0:
            raise BoardPositionAlreadyTaken

        self._current_step += 1
        current_stone = Stone(action, self._current_stone_color, self._current_step)
        self._stone_array.append(current_stone)

        self._board_state[row][col] = self._current_stone_color.value
        self._board_stone[row][col] = current_stone
        self._board_patterns.add_stone(current_stone)
        have_five = self._board_patterns.five_stones_found
        is_full = self._current_step >= self._board_size ** 2
        if not(have_five or is_full):
            self._current_stone_color = self._current_stone_color.next()

        return have_five, is_full

    def render(self, mode='human'):
        """
        :param mode: choose render mode
        :return: figure or rgb_array
        """
        if mode == 'human':
            fig = plt.figure(figsize=[8, 8])
            ax = fig.add_subplot(111, xticks=range(self._board_size), yticks=range(self._board_size),
                                 position=[.1, .1, .8, .8])
            ax.grid(color='k', linestyle='-', linewidth=1)
            ax.xaxis.set_tick_params(bottom='off', top='off', labelbottom='off')
            ax.yaxis.set_tick_params(left='off', right='off', labelleft='off')
            for stone in self._stone_array:
                ax.add_patch(stone.get_mpatches())
                stone.draw_step_number()
            plt.show()
        else:
            pass

    def position_exist(self, row, col):
        return 0 <= row < self.board_size and 0 <= col < self.board_size

    @property
    def board_size(self):
        return self._board_size

    @property
    def board_state(self):
        return self._board_state

    @property
    def board_stone(self):
        return self._board_stone

    @property
    def stone_array(self):
        return self._stone_array

    @property
    def board_patterns(self):
        return self._board_patterns

    @property
    def current_stone_color(self):
        return self._current_stone_color
