import gym
from gym import spaces
import numpy as np
from gomoku.envs.board import Board
from gomoku.envs.boardUtils import StoneColor
from gomoku.envs.opponent import RandomAgent


class GomokuEnv(gym.Env):
    def __init__(self, board_size=15, opponent=None):
        self._board_size = board_size
        self._board = Board(board_size)
        if opponent is None:
            # opponent uses white stone
            self.opponent = RandomAgent(self._board, StoneColor.white)
        else:
            self.opponent = None

        self.action_space = spaces.MultiDiscrete([board_size, board_size])
        self.observation_space = spaces.Box(-1, 1, (board_size, board_size), dtype=np.int8)

    def reset(self):
        self._board.reset()
        return self._get_obs()

    def _get_obs(self):
        return self._board.board_state

    def render(self, mode='human'):
        self._board.render(mode)

    def step(self, action):
        """
        step the environment
        :param action: [row, column] specify the position for the current stone to be placed
        :return: observation, reward, done, information
        """
        reward = 0
        info = {}

        # punish invalid action, i.e. put stone on other stones
        row, col = action
        if self._board.board_state[row][col] != 0:
            return self._get_obs(), -1000, True, info

        # TODO: validate the action
        have_five, is_full = self._board.step(action)
        reward = 1000 if have_five else 0

        if not (have_five or is_full):
            opponent_action, _ = self.opponent.predict(self._get_obs())
            have_five, is_full = self._board.step(opponent_action)
            reward = -1000 if have_five else 0

        done = have_five or is_full

        return self._get_obs(), reward, done, info

    @property
    def board_size(self):
        return self._board_size

    @property
    def board(self):
        return self._board
