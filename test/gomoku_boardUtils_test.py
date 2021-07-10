import pytest

from gomoku.envs.board import Board
from gomoku.envs.boardUtils import Orientation, StoneColor

BLACK = StoneColor.black
WHITE = StoneColor.white


def test_Pattern_end_stones():
    board = Board()
    board.step([7, 7])
    pattern0 = board.board_patterns.black_stone_patterns[0]
    assert pattern0.end_stones[0] == board.stone_array[0]
    assert pattern0.end_stones[1] == board.stone_array[0]
    board.step([7, 12])
    board.step([8, 7])
    assert pattern0.end_stones[0] == board.stone_array[0]
    assert pattern0.end_stones[1] == board.stone_array[2]
    board.step([6, 12])
    pattern1 = board.board_patterns.white_stone_patterns[0]
    assert pattern1.end_stones[0] == board.stone_array[3]
    assert pattern1.end_stones[1] == board.stone_array[1]
    board.step([6, 7])
    assert pattern0.end_stones[0] == board.stone_array[4]
    assert pattern0.end_stones[1] == board.stone_array[2]
    # board.render()


def test_Pattern_end_stones_next_position():
    board = Board()
    board.step([7, 7])
    pattern0 = board.board_patterns.black_stone_patterns[0]
    assert pattern0.end_stones_next_position(board) == [None, None]
    board.step([7, 12])
    board.step([8, 7])
    assert pattern0.end_stones_next_position(board) == [[6, 7], [9, 7]]
    board.step([7, 11])
    pattern1 = board.board_patterns.white_stone_patterns[0]
    assert pattern1.end_stones_next_position(board) == [[7, 10], [7, 13]]
    board.step([6, 7])
    assert pattern0.end_stones_next_position(board) == [[5, 7], [9, 7]]
    board.step([7, 13])
    board.step([5, 7])
    board.step([7, 14])
    assert pattern1.end_stones_next_position(board) == [[7, 10], None]
    # board.render()


def test_BoardPattern_update_patterns_end_free():
    board = Board()
    board.step([7, 7])
    board.step([7, 8])
    board.step([8, 7])
    board.step([7, 9])
    pattern0 = board.board_patterns.black_stone_patterns[0]
    pattern1 = board.board_patterns.white_stone_patterns[0]
    assert pattern0.min_stone_free and pattern0.max_stone_free
    assert (not pattern1.min_stone_free) and pattern1.max_stone_free
    board.step([9, 7])
    board.step([8, 8])
    assert pattern0.min_stone_free and pattern0.max_stone_free
    pattern2 = board.board_patterns.white_stone_patterns[0]
    assert pattern2.min_stone_free and pattern2.max_stone_free
    assert pattern2.number_of_stones == 2
    assert pattern2.orientation == Orientation.horizontal
    board.step([7, 5])
    board.step([10, 7])
    board.step([7, 10])
    board.step([6, 7])
    pattern3 = board.board_patterns.black_stone_patterns[-1]
    assert not pattern3.min_stone_free and not pattern3.max_stone_free
    assert pattern3.free_end_number == 0
    assert pattern3.number_of_stones == 3
    assert pattern3.orientation == Orientation.horizontal
    pattern4 = board.board_patterns.white_stone_patterns[-1]
    assert not pattern4.min_stone_free and not pattern4.max_stone_free
    assert pattern4.number_of_stones == 2
    assert pattern4.orientation == Orientation.vertical

    # print("")
    # print(board.board_patterns.black_stone_patterns)
    # print(board.board_patterns.white_stone_patterns)
    # board.render()
