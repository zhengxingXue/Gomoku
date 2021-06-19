import gym
import enum
import numpy as np


class Stone(enum.Enum):
    black = 1
    white = -1

    def turn(self):
        return Stone.black if self == Stone.white else Stone.white


class GomokuEnv(gym.Env):
    def __init__(self, board_size=15):
        self._board_size = board_size
        self._board = np.zeros((self._board_size, self._board_size), dtype=int)
        self._current_stone = Stone.black

    def reset(self):
        self._board = np.zeros((self._board_size, self._board_size), dtype=int)
        self._current_stone = Stone.black
        return self._get_obs()

    def _get_obs(self):
        return self._board

    def render(self, mode='human'):
        if mode == 'human':
            render_dict = {-1: "O", 1: "X", 0: " "}
            print(' ')
            for row in range(self._board_size):
                print('{row:2d} |'.format(row=row), end="")
                for col in range(self._board_size):
                    print(render_dict[self._board[row][col]], end="|")
                print(' ')
        else:
            pass

    def step(self, action):
        """
        step the environment
        :param action: [row, column] specify the position for the current stone to be placed
        :return: observation, reward, done, information
        """
        reward = 0
        info = {}

        # TODO: validate the action
        (row, col) = action

        # place current stone
        self._board[row][col] = self._current_stone.value

        # check if there is five stones in a row
        done = self._have_five(action)

        # change the current stone
        self._current_stone = self._current_stone.turn()

        return self._get_obs(), reward, done, info

    def _count_on_direction(self, action, direction):
        """
        helper for counting stones
        :param action: [row, column]
        :param direction: [row_direction, col_direction]
        :return: the number of stones in the direction that matches the current stone
        """
        count = 0
        (row, col) = action
        (row_direction, col_direction) = direction
        for step in range(1, 5):
            temp_row = row + row_direction * step
            temp_col = col + col_direction * step
            if (temp_row < 0 or temp_row >= self._board_size) or (temp_col < 0 or temp_col >= self._board_size):
                break
            if self._board[temp_row][temp_col] == self._current_stone.value:
                count += 1
            else:
                break
        return count

    def _have_five(self, action):
        """
        check if the board have five stones in a row
        :param action: [row, column]
        :return: whether the board have five stones in a row
        """
        directions = [[(-1, 0), (1, 0)],
                      [(0, -1), (0, 1)],
                      [(-1, 1), (1, -1)],
                      [(-1, -1), (1, 1)]]
        for axis in directions:
            axis_count = 1
            for direction in axis:
                axis_count += self._count_on_direction(action, direction)
                if axis_count >= 5:
                    return True
        return False

    @property
    def board_size(self):
        return self._board_size

    @property
    def board(self):
        return self._board

    @property
    def current_stone(self):
        return self._current_stone
