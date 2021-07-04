import gym
import enum
import numpy as np
from gomoku.envs.board import Board


class GomokuEnv(gym.Env):
    def __init__(self, board_size=15):
        self._board_size = board_size
        self._board = Board(board_size)

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

        # TODO: validate the action
        done = self._board.step(action)

        return self._get_obs(), reward, done, info

    @property
    def board_size(self):
        return self._board_size

    @property
    def board(self):
        return self._board
