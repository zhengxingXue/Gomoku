import pytest
from gomoku.envs import GomokuEnv
from gomoku.envs.boardUtils import StoneColor
from gomoku.envs.opponent import RandomAgent, EasyAgent


def test_RandomAgent():
    env = GomokuEnv()
    opponent = RandomAgent(env.board, StoneColor.white)
    env.opponent = opponent
    # Can fail
    try:
        for i in range(5):
            _, _, done, _ = env.step([i + 4, 7])
    except:
        pass
    # assert done
    # env.render()


def test_EasyAgent():
    env = GomokuEnv()
    opponent = EasyAgent(env.board, StoneColor.white, randomness=False)
    env.opponent = opponent
    env.step([7, 7])
    env.step([7, 6])
    env.step([7, 8])
    env.step([7, 9])
    # env.render()
    # print("")
    # print(env.board.board_patterns)
    # print(env.board.stone_array[7])
