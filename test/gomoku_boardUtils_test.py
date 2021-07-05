import pytest

from gomoku.envs.board import Board
from gomoku.envs.boardUtils import Orientation, StoneColor

BLACK = StoneColor.black
WHITE = StoneColor.white


def pattern_helper_get_end_stones(pattern, index):
    return pattern.end_stones[index]


def test_Pattern_end_stones():
    board = Board()
    board.step([7, 7])
    pattern0 = board.board_patterns.black_stone_patterns[0]
    assert pattern_helper_get_end_stones(pattern0, 0) == board.stone_array[0]
    assert pattern_helper_get_end_stones(pattern0, 1) == board.stone_array[0]
    board.step([7, 12])
    board.step([8, 7])
    assert pattern_helper_get_end_stones(pattern0, 0) == board.stone_array[0]
    assert pattern_helper_get_end_stones(pattern0, 1) == board.stone_array[2]
    board.step([6, 12])
    pattern1 = board.board_patterns.white_stone_patterns[0]
    assert pattern_helper_get_end_stones(pattern1, 0) == board.stone_array[3]
    assert pattern_helper_get_end_stones(pattern1, 1) == board.stone_array[1]
    board.step([6, 7])
    assert pattern_helper_get_end_stones(pattern0, 0) == board.stone_array[4]
    assert pattern_helper_get_end_stones(pattern0, 1) == board.stone_array[2]
    # board.render()
