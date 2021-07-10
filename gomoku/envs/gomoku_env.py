import gym
from gym import spaces
import numpy as np
from gomoku.envs.board import Board
from gomoku.envs.boardUtils import StoneColor
from gomoku.envs.opponent import RandomAgent


def _black_stone_reward_from_patterns(patterns, patterns_color):
    reward = 0
    for pattern in patterns:
        reward += pattern.number_of_stones ** 2
    return reward if patterns_color == StoneColor.black else -reward


class GomokuEnv(gym.Env):
    def __init__(self, board_size=15, opponent_class=RandomAgent):
        self._board_size = board_size
        self._board = Board(board_size)

        # opponent uses white stone
        self.opponent = opponent_class(self._board, StoneColor.white)

        self.action_space = spaces.Discrete(board_size ** 2)
        # self.action_space = spaces.MultiDiscrete([board_size, board_size])
        self.observation_space = spaces.Box(-1, 1, (board_size**2,), dtype=np.int8)

    def reset(self):
        self._board.reset()
        return self._get_obs()

    def _get_obs(self):
        return self._board.board_state.flatten()

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

        if isinstance(action, int) or isinstance(action, np.int64):
            row = action // self._board_size
            col = action % self._board_size
            action = [row, col]
        else:
            row, col = action
        # punish invalid action, i.e. put stone on other stones
        # end env after such action
        if self._board.board_state[row][col] != 0:
            return self._get_obs(), -1000, True, info

        # TODO: validate the action
        have_five, is_full = self._board.step(action)
        reward += 1000 if have_five else 0

        # reward actions that link the stones
        reward += _black_stone_reward_from_patterns(self._board.board_patterns.black_stone_patterns, StoneColor.black)

        if not (have_five or is_full):
            opponent_action, _ = self.opponent.predict(self._get_obs())
            have_five, is_full = self._board.step(opponent_action)
            reward -= 1000 if have_five else 0

        done = have_five or is_full

        return self._get_obs(), reward, done, info

    @property
    def board_size(self):
        return self._board_size

    @property
    def board(self):
        return self._board
