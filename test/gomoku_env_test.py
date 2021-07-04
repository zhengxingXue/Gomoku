import pytest
import gym

from gomoku.envs import GomokuEnv


def test_gym_make():
    env = gym.make("gomoku-v0")
    assert env.board_size == 15


def test_GomokuEnv_init():
    env = GomokuEnv()
    assert env.board_size == 15
