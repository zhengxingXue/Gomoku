import pytest
import gym
from stable_baselines3.common.env_checker import check_env
from gomoku.envs import GomokuEnv


def test_gym_make():
    env = gym.make("gomoku-v0")
    check_env(env)
    assert env.board_size == 15


def test_GomokuEnv_init():
    env = GomokuEnv()
    check_env(env)
    assert env.board_size == 15
    env.step(0)
    # env.render()


def test_env_step():
    env = GomokuEnv()
    obs, reward, done, info = env.step([7, 7])
    assert obs.shape == (15 ** 2,)
    assert reward == 1
    assert done is False
    assert info == {}
    # env.render()


def test_env_BoardPositionAlreadyTaken():
    env = GomokuEnv()
    env.step([7, 7])
    _, _, done, _ = env.step([7, 7])
    assert done is True
    env.render()
