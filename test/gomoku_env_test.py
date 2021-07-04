import pytest
import gym

from gomoku.envs import GomokuEnv


def test_gym_make():
    env = gym.make("gomoku-v0")
    assert env.board_size == 15


def test_GomokuEnv_init():
    env = GomokuEnv()
    assert env.board_size == 15


def test_env_step():
    env = GomokuEnv()
    obs, reward, done, info = env.step([7, 7])
    assert obs.shape == (15, 15)
    assert reward == 1
    assert done is False
    assert info == {}
    # env.render()
