import pytest
import gym

from gomoku.envs import GomokuEnv, Stone


def test_gym_make():
    env = gym.make("gomoku-v0")
    assert env.board_size == 15
    assert env.current_stone == Stone.black


def test_GomokuEnv_simple():
    env = GomokuEnv()
    assert env.board_size == 15
    assert env.current_stone == Stone.black
    env.step([0, 0])
    assert env.current_stone == Stone.white
    env.reset()
    assert env.board_size == 15
    assert env.current_stone == Stone.black


def test_GomokuEnv_five_in_a_row():
    env = GomokuEnv()
    b = env.board_size
    action_list_edges = [[0, 0], [0, b - 1], [b - 1, b - 1], [b - 1, 0], [0, 2]]
    action_list_horizontal_five = [[7, 3], [7, 4], [7, 5], [7, 6], [7, 7]]
    action_list_vertical_five = [[3, 7], [4, 7], [5, 7], [6, 7], [7, 7]]
    action_list_diagonal_left_five = [[2, 2], [3, 3], [4, 4], [5, 5], [6, 6]]
    action_list_diagonal_right_five = [[2, 8], [3, 7], [4, 6], [5, 5], [6, 4]]
    action_list_list = [action_list_edges,
                        action_list_horizontal_five,
                        action_list_vertical_five,
                        action_list_diagonal_left_five,
                        action_list_diagonal_right_five]
    for lst1 in action_list_list:
        for lst2 in action_list_list:
            if lst1 != lst2:
                for i in range(5):
                    _, _, done, _ = env.step(lst1[i])
                    if done:
                        break
                    _, _, done, _ = env.step(lst2[i])
                    if done:
                        break
                assert done is True
                # env.render()
                env.reset()


def test_render():
    env = GomokuEnv()
    env.step([8, 7])
    env.step([8, 8])
    env.render()
