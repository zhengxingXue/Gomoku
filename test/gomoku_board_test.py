import pytest

from gomoku.envs.board import Board
from gomoku.envs.boardUtils import Orientation, StoneColor

BLACK = StoneColor.black
WHITE = StoneColor.white


# coverage run -m pytest; coverage html

def test_Board_init():
    b = Board()
    assert b.board_size == 15
    assert len(b.stone_array) == 0
    assert b.board_stone == [[0] * 15 for _ in range(15)]
    assert len(b.board_patterns.black_stone_patterns) == 0
    assert len(b.board_patterns.white_stone_patterns) == 0
    assert b.board_patterns.five_stones_found is False
    have_five, is_full = b.step([7, 7])
    assert have_five is False
    assert is_full is False


def boardPattern_check_patterns_length(board, b_l, w_l):
    assert len(board.board_patterns.black_stone_patterns) == b_l
    assert len(board.board_patterns.white_stone_patterns) == w_l


def boardPattern_check_pattern_attr_stones(pattern, stone_array, stone_color):
    for stone in pattern.stones:
        assert stone in stone_array
        assert pattern in stone.patterns
        assert stone.color == stone_color


def boardPattern_check_pattern_attr(pattern, orientation, color, number_of_stones):
    assert pattern.orientation == orientation
    assert pattern.color == color
    assert pattern.number_of_stones == number_of_stones


def boardPattern_orientation_helper(board, orientation, b_l, w_l, pattern, stone_color, number_of_stones, stone_array):
    boardPattern_check_patterns_length(board, b_l, w_l)
    boardPattern_check_pattern_attr(pattern, orientation, stone_color, number_of_stones)
    boardPattern_check_pattern_attr_stones(pattern, stone_array, stone_color)


def test_Board_step_boardPattern_any():
    orientation = Orientation.any
    board = Board()
    board.step([7, 7])
    pattern0 = board.board_patterns.black_stone_patterns[0]
    stone_array0 = [board.stone_array[0]]
    boardPattern_orientation_helper(board, orientation, 1, 0, pattern0, BLACK, 1, stone_array0)
    board.step([7, 12])
    pattern1 = board.board_patterns.white_stone_patterns[0]
    stone_array1 = [board.stone_array[1]]
    boardPattern_orientation_helper(board, orientation, 1, 1, pattern0, BLACK, 1, stone_array0)
    boardPattern_orientation_helper(board, orientation, 1, 1, pattern1, WHITE, 1, stone_array1)
    board.step([7, 9])
    pattern2 = board.board_patterns.black_stone_patterns[1]
    stone_array2 = [board.stone_array[2]]
    boardPattern_orientation_helper(board, orientation, 2, 1, pattern0, BLACK, 1, stone_array0)
    boardPattern_orientation_helper(board, orientation, 2, 1, pattern1, WHITE, 1, stone_array1)
    boardPattern_orientation_helper(board, orientation, 2, 1, pattern2, BLACK, 1, stone_array2)
    # board.render()


def test_Board_step_boardPattern_horizontal():
    orientation = Orientation.horizontal
    board = Board()
    board.step([7, 7])
    board.step([7, 12])
    board.step([8, 7])
    pattern0 = board.board_patterns.black_stone_patterns[0]
    stone_array0 = [board.stone_array[0], board.stone_array[2]]
    boardPattern_orientation_helper(board, orientation, 1, 1, pattern0, BLACK, 2, stone_array0)
    board.step([9, 12])
    board.step([6, 7])
    stone_array0 += [board.stone_array[4]]
    boardPattern_orientation_helper(board, orientation, 1, 2, pattern0, BLACK, 3, stone_array0)
    board.step([8, 12])
    pattern1 = board.board_patterns.white_stone_patterns[0]
    # be careful of the sequence of the stones
    stone_array1 = [board.stone_array[1], board.stone_array[5], board.stone_array[3]]
    boardPattern_orientation_helper(board, orientation, 1, 1, pattern1, WHITE, 3, stone_array1)
    # board.render()


def test_Board_step_boardPattern_check_orientation_edge_case0():
    board = Board()
    board.step([7, 7])
    board.step([7, 12])
    board.step([8, 7])
    pattern0 = board.board_patterns.black_stone_patterns[0]
    stone_array0 = [board.stone_array[0], board.stone_array[2]]
    boardPattern_orientation_helper(board, Orientation.horizontal, 1, 1, pattern0, BLACK, 2, stone_array0)
    board.step([7, 11])
    pattern1 = board.board_patterns.white_stone_patterns[0]
    stone_array1 = [board.stone_array[1], board.stone_array[3]]
    boardPattern_orientation_helper(board, Orientation.vertical, 1, 1, pattern1, WHITE, 2, stone_array1)
    board.step([7, 6])
    pattern2 = board.board_patterns.black_stone_patterns[1]
    stone_array2 = [board.stone_array[0], board.stone_array[4]]
    boardPattern_orientation_helper(board, Orientation.vertical, 3, 1, pattern2, BLACK, 2, stone_array2)
    pattern3 = board.board_patterns.black_stone_patterns[2]
    stone_array3 = [board.stone_array[2], board.stone_array[4]]
    boardPattern_orientation_helper(board, Orientation.right_diagonal, 3, 1, pattern3, BLACK, 2, stone_array3)
    board.step([5, 11])
    board.step([8, 6])
    pattern4 = board.board_patterns.black_stone_patterns[3]
    stone_array4 = [board.stone_array[4], board.stone_array[6]]
    pattern5 = board.board_patterns.black_stone_patterns[4]
    stone_array5 = [board.stone_array[2], board.stone_array[6]]
    pattern6 = board.board_patterns.black_stone_patterns[5]
    stone_array6 = [board.stone_array[0], board.stone_array[6]]
    for orientation, pattern, stone_array in zip([Orientation.horizontal, Orientation.vertical,
                                                  Orientation.right_diagonal, Orientation.horizontal,
                                                  Orientation.vertical, Orientation.left_diagonal],
                                                 [pattern0, pattern2, pattern3, pattern4, pattern5, pattern6],
                                                 [stone_array0, stone_array2, stone_array3,
                                                  stone_array4, stone_array5, stone_array6]):
        boardPattern_orientation_helper(board, orientation, 6, 2, pattern, BLACK, 2, stone_array)
    # board.render()


def test_Board_step_boardPattern_check_orientation_edge_case1():
    board = Board()
    board.step([7, 7])
    board.step([7, 12])
    board.step([8, 7])
    board.step([9, 12])
    board.step([7, 5])
    pattern0 = board.board_patterns.black_stone_patterns[0]
    stone_array0 = [board.stone_array[0], board.stone_array[2]]
    boardPattern_orientation_helper(board, Orientation.horizontal, 2, 2, pattern0, BLACK, 2, stone_array0)
    board.step([11, 12])
    board.step([7, 6])
    pattern0 = board.board_patterns.black_stone_patterns[0]
    stone_array0 = [board.stone_array[0], board.stone_array[6], board.stone_array[4]]
    pattern1 = board.board_patterns.black_stone_patterns[1]
    stone_array1 = [board.stone_array[0], board.stone_array[2]]
    pattern2 = board.board_patterns.black_stone_patterns[2]
    stone_array2 = [board.stone_array[2], board.stone_array[6]]
    boardPattern_orientation_helper(board, Orientation.vertical, 3, 3, pattern0, BLACK, 3, stone_array0)
    boardPattern_orientation_helper(board, Orientation.horizontal, 3, 3, pattern1, BLACK, 2, stone_array1)
    boardPattern_orientation_helper(board, Orientation.right_diagonal, 3, 3, pattern2, BLACK, 2, stone_array2)
    # board.render()


def test_Board_step_boardPattern_check_dr_dc_edge_case0():
    board = Board()
    board.step([0, 0])
    board.step([14, 14])
    board.step([1, 0])
    pattern0 = board.board_patterns.black_stone_patterns[0]
    stone_array0 = [board.stone_array[0], board.stone_array[2]]
    boardPattern_orientation_helper(board, Orientation.horizontal, 1, 1, pattern0, BLACK, 2, stone_array0)
    board.step([13, 14])
    pattern1 = board.board_patterns.white_stone_patterns[0]
    stone_array1 = [board.stone_array[1], board.stone_array[3]]
    boardPattern_orientation_helper(board, Orientation.horizontal, 1, 1, pattern1, WHITE, 2, stone_array1)
    # board.render()


def test_Board_step_boardPattern_five_stones_found():
    board = Board()
    for i in range(5):
        have_five, is_full = board.step([i+5, 7])
        assert have_five is (True if i == 4 else False)
        assert is_full is False
        have_five, is_full = board.step([i+3, 11])
        assert have_five is (True if i == 4 else False)
        assert is_full is False
    # board.render()


def test_Board_render():
    b = Board()
    b.step([7, 7])
    b.step([8, 7])
    b.step([7, 8])
    b.render()
    print(b.board_patterns.black_stone_patterns[0])

# coverage run -m pytest; coverage html
