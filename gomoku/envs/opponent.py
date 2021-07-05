import random
from gomoku.envs.boardUtils import StoneColor, Orientation


class Agent(object):
    def __init__(self, board, stone_color):
        self._board = board
        self.stone_color = stone_color

    @property
    def board(self):
        return self._board


class RandomAgent(Agent):
    def __init__(self, board, stone_color):
        Agent.__init__(self, board, stone_color)

    def predict(self, obs=None):
        not_found = True
        # Optimize
        while not_found:
            row = self._random_rc()
            col = self._random_rc()
            not_found = self._board.board_state[row][col] != 0
        return [row, col], None

    def _random_rc(self):
        return random.randint(0, self._board.board_size - 1)


class EasyAgent(Agent):
    def __init__(self, board, stone_color):
        Agent.__init__(self, board, stone_color)

    def predict(self, obs=None):
        if len(self.patterns) == 0:
            if len(self.opponent_patterns) == 0:
                # No pattern, i.e. start of the game
                # Place stone in middle
                return [self._board.board_size // 2, self._board.board_size // 2], None
            else:
                available_positions = self._check_stone_surroundings(
                    self.opponent_patterns[0].stones[0],
                    Orientation.any
                )
                # TODO: change
                chosen_position = available_positions[0]
                return chosen_position, None
        else:
            chosen_position = None
            chosen_pattern_index = 0
            # ATTACK, expand the existing pattern
            while chosen_position is None and chosen_pattern_index < len(self.patterns):
                chosen_pattern = self.patterns[chosen_pattern_index]
                min_stone, max_stone = chosen_pattern.end_stones
                for stone in [min_stone, max_stone]:
                    available_positions = self._check_stone_surroundings(
                        stone,
                        chosen_pattern.orientation
                    )
                    if len(available_positions) != 0:
                        chosen_position = available_positions[0]
                        return chosen_position, None
                # No available position around the end stones in the pattern
                # check every stone in the longest pattern in any orientation
                for stone in chosen_pattern.stones:
                    available_positions = self._check_stone_surroundings(
                        stone,
                        Orientation.any
                    )
                    if len(available_positions) != 0:
                        chosen_position = available_positions[0]
                        return chosen_position, None
                chosen_pattern_index += 1
            # DEFENCE, block opponent
            # TODO: Implement
            return [-1, -1], None

    def _check_stone_surroundings(self, stone, orientation):
        row, col = stone.position
        available_positions = []
        if orientation == Orientation.horizontal or orientation == Orientation.any:
            available_positions += self._check_stone_surroundings_in(row, col, [-1, 0], [1, 0])
        if orientation == Orientation.vertical or orientation == Orientation.any:
            available_positions += self._check_stone_surroundings_in(row, col, [0, 1], [0, -1])
        if orientation == Orientation.left_diagonal or orientation == Orientation.any:
            available_positions += self._check_stone_surroundings_in(row, col, [-1, 1], [1, -1])
        if orientation == Orientation.right_diagonal or orientation == Orientation.any:
            available_positions += self._check_stone_surroundings_in(row, col, [-1, -1], [1, 1])
        return available_positions

    def _check_stone_surroundings_in(self, row, col, o1, o2):
        available_position = []
        for dr, dc in [o1, o2]:
            if self._check_empty_in_dr_dc(row, col, dr, dc):
                available_position.append((row + dr, col + dc))
        return available_position

    # TODO: Copied code
    def _position_exist(self, row, col):
        return 0 <= row < self._board.board_size and 0 <= col < self._board.board_size

    def _check_empty_in_dr_dc(self, row, col, dr, dc):
        row += dr
        col += dc
        if self._position_exist(row, col):
            return self._board.board_state[row][col] == 0
        else:
            return False

    @property
    def opponent_patterns(self):
        if self.stone_color == StoneColor.black:
            return self._board.board_patterns.white_stone_patterns
        else:
            return self._board.board_patterns.black_stone_patterns

    @property
    def patterns(self):
        if self.stone_color == StoneColor.black:
            return self._board.board_patterns.black_stone_patterns
        else:
            return self._board.board_patterns.white_stone_patterns
