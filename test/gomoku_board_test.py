import pytest

from gomoku.envs.board import Board
from gomoku.envs.boardUtils import Orientation, StoneColor


RENDER = True


def test_Board_init():
    b = Board()
    assert b.board_size == 15
    assert len(b.stone_array) == 0
    assert b.board_stone == [[0] * 15 for _ in range(15)]
    assert len(b.board_patterns.black_stone_patterns) == 0
    assert len(b.board_patterns.white_stone_patterns) == 0
    assert b.board_patterns.five_stones_found is False
    done = b.step([7, 7])
    assert done is False


def boardPattern_any_helper(board, position, stone_color, step, b_l, w_l, pattern):
    assert len(board.board_patterns.black_stone_patterns) == b_l
    assert len(board.board_patterns.white_stone_patterns) == w_l
    assert pattern.color == stone_color
    assert pattern.number_of_stones == 1
    assert pattern.orientation == Orientation.any
    assert pattern.stones[0].position == position
    assert pattern.stones[0].step == step
    assert pattern.stones[0].color == stone_color


def test_Board_step_boardPattern_any():
    board = Board()
    board.step([7, 7])
    pattern0 = board.board_patterns.black_stone_patterns[0]
    boardPattern_any_helper(board, [7, 7], StoneColor.black, 1, 1, 0, pattern0)
    board.step([7, 12])
    pattern1 = board.board_patterns.white_stone_patterns[0]
    boardPattern_any_helper(board, [7, 7], StoneColor.black, 1, 1, 1, pattern0)
    boardPattern_any_helper(board, [7, 12], StoneColor.white, 2, 1, 1, pattern1)
    if RENDER: board.render()


def test_Board_step_boardPattern_horizontal():
    board = Board()
    board.step([7, 7])
    board.step([7, 12])

    if RENDER: board.render()


def test_Board_render():
    b = Board()
    b.step([7, 7])
    b.step([8, 7])
    b.step([7, 8])
    b.render()
