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
    def __init__(self, board, stone_color, randomness=False):
        Agent.__init__(self, board, stone_color)
        self._available_positions = []
        self._randomness = randomness

    def predict(self, obs=None):
        self._update_available_position()
        chosen_pos = random.choice(self._available_positions) if self._randomness \
            else self._available_positions[0]
        self._available_positions = []  # reset the available positions
        return chosen_pos, None

    def _update_available_position(self):
        if len(self.patterns) == 0:
            if len(self.opponent_patterns) == 0:
                # No pattern, i.e. start of the game
                # Place stone in middle
                self._available_positions = [
                    [self._board.board_size // 2, self._board.board_size // 2]
                ]
            else:
                # Only opponent stone, place stone around the opponent
                self._available_positions = self._check_stone_surroundings(
                    self.opponent_patterns[0].stones[0],
                    Orientation.any
                )
        else:
            if self._need_defence():
                # DEFENCE
                # as the pattern has more than 1 free end to need defence,
                # the _available_positions should have at least one item
                self._update_available_position_based_on_free_end(self.opponent_patterns[0])
            else:
                # ATTACK
                pattern_index = 0
                pattern_index_limit = len(self.patterns)
                # go through the patterns and find available_positions in free end
                while len(self._available_positions) == 0 and pattern_index < pattern_index_limit:
                    current_pattern = self.patterns[pattern_index]
                    if current_pattern.orientation == Orientation.any:
                        self._available_positions = self._check_stone_surroundings(
                            current_pattern.stones[0],
                            Orientation.any
                        )
                    else:
                        if current_pattern.free_end_number > 0:
                            # has free end stone, use the free end
                            self._update_available_position_based_on_free_end(current_pattern)
                        else:
                            # no free end stone, check next
                            # TODO: Test, may not work
                            pass
                    pattern_index += 1

                pattern_index = 0
                # go through the patterns and find available_positions in any position of
                # the stones in pattern
                while len(self._available_positions) == 0 and pattern_index < pattern_index_limit:
                    current_pattern = self.patterns[pattern_index]

                    for stone in current_pattern.stones:
                        self._available_positions = self._check_stone_surroundings(
                            stone,
                            Orientation.any
                        )

                    pattern_index += 1

                # cannot find any available positions, get a random positions,
                # should not happen (often)
                if len(self._available_positions) == 0:
                    temp_agent = RandomAgent(self.board, self.stone_color)
                    pos, _ = temp_agent.predict()
                    self._available_positions = [pos]

    def _need_defence(self):
        # if the agent longest pattern has 4 stones and free end, attack and win
        if self.patterns[0].number_of_stones >= 4 and self.patterns[0].free_end_number > 0:
            return False
        # opponent longest pattern has more than 3 stones and has more than 1 free end
        # or more than 4 stones and has more than 0 free end, need defence
        opponent_longest_pattern = self.opponent_patterns[0]
        opponent_ns = opponent_longest_pattern.number_of_stones
        opponent_fe = opponent_longest_pattern.free_end_number
        need_defence = (opponent_ns >= 4 and opponent_fe > 0) or (opponent_ns >= 3 and opponent_fe > 1)
        return need_defence

    def _update_available_position_based_on_free_end(self, pattern):
        positions = pattern.end_stones_next_position(self._board)
        for position in positions:
            if position is not None:
                self._available_positions += [position]

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

    def _check_empty_in_dr_dc(self, row, col, dr, dc):
        row += dr
        col += dc
        if self._board.position_exist(row, col):
            return self._board.board_state[row][col] == 0
        else:
            return False

    @property
    def available_position(self):
        return self._available_positions

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
