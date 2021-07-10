import enum
import matplotlib.patches as mpatches
import matplotlib.pyplot as plt


class StoneColor(enum.Enum):
    black = 1
    white = -1

    def next(self):
        return StoneColor.black if self == StoneColor.white else StoneColor.white


class Stone(object):
    def __init__(self, position, color, step):
        self._position = position
        assert color == StoneColor.black or color == StoneColor.white, "invalid color type"
        self._color = color
        self._step = step
        self.patterns = []

    def __repr__(self):
        rep = "Stone "
        rep += str(self._step) + " "
        rep += "b " if self._color == StoneColor.black else "w "
        rep += "[" + str(self._position[0]) + ", " + str(self._position[1]) + "] "
        return rep

    def get_mpatches(self):
        x, y = self.position
        facecolor = (0, 0, 0) if self._color == StoneColor.black else (1, 1, 1)
        radius = 0.45
        zorder = 10
        return mpatches.Circle((x, y), radius, facecolor=facecolor, edgecolor=(0, 0, 0), linewidth=1, clip_on=False,
                               zorder=zorder)

    def draw_step_number(self):
        x, y = self.position
        color = (1, 1, 1) if self._color == StoneColor.black else (0, 0, 0)
        plt.text(x, y, str(self._step), size=15, color=color, ha="center", va="center", zorder=20)

    def get_pattern(self, orientation):
        pattern_any = 0
        for pattern in self.patterns:
            if pattern.orientation == orientation:
                return pattern
            elif pattern.orientation == Orientation.any:
                pattern_any = pattern
                break
        if pattern_any == 0:
            pattern = Pattern(self)
        else:
            pattern = pattern_any
        pattern.orientation = orientation
        return pattern

    # def __eq__(self, other):
    #     if isinstance(other, Stone):
    #         return self.position == other.position and self.color == other.color and self.step == other.step
    #     return False

    def __lt__(self, other):
        if isinstance(other, Stone):
            return (self.position[0], self.position[1]) < (other.position[0], other.position[1])
        return False

    @property
    def position(self):
        return self._position

    @property
    def color(self):
        return self._color

    @property
    def step(self):
        return self._step


class Orientation(enum.Enum):
    any = "any"
    horizontal = "horizontal"
    vertical = "vertical"
    left_diagonal = "left_diagonal"
    right_diagonal = "right_diagonal"


Orientation_dictionary = {
    Orientation.horizontal: [[-1, 0], [1, 0]],
    Orientation.vertical: [[0, -1], [0, 1]],
    Orientation.left_diagonal: [[-1, 1], [1, -1]],
    Orientation.right_diagonal: [[-1, -1], [1, 1]]
}


class StoneArray(list):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def append(self, val):
        index = 0
        for item in self:
            if val < item:
                break
            index += 1
        self.insert(index, val)


class Pattern(object):
    def __init__(self, stone):
        self._color = stone.color
        self.orientation = Orientation.any
        self.stones = StoneArray([stone])

        self.min_stone_free = True
        self.max_stone_free = True

        stone.patterns.append(self)

    def end_stones_next_position(self, board):
        min_stone, max_stone = self.end_stones
        if self.orientation == Orientation.any:
            return [None, None]
        result = []
        for stone, free, (dr, dc) in zip(
                [min_stone, max_stone],
                [self.min_stone_free, self.max_stone_free],
                Orientation_dictionary[self.orientation]
        ):
            row, col = stone.position
            if board.position_exist(row + dr, col + dc) and free:
                result += [[row + dr, col + dc]]
            else:
                result += [None]
        return result

    def __repr__(self):
        rep = "b " if self._color == StoneColor.black else "w "
        rep += str(self.number_of_stones) + " "
        rep += self.orientation.value + " "
        rep += "["
        for stone in self.stones:
            rep += str(stone.step) + " "
        rep = rep[:-1]
        rep += "] "
        rep += str(self.min_stone_free) + " "
        rep += str(self.max_stone_free)
        return rep

    def __lt__(self, other):
        return (self.free_end_number != 0, self.number_of_stones, self.free_end_number) < \
               (other.free_end_number != 0, other.number_of_stones, other.free_end_number)

    @property
    def color(self):
        return self._color

    @property
    def number_of_stones(self):
        return len(self.stones)

    @property
    def end_stones(self):
        return self.stones[0], self.stones[-1]

    @property
    def free_end_number(self):
        return int(self.max_stone_free) + int(self.min_stone_free)


def _update_pattern_along_orientation(existing_stone, orientation, stone, patterns):
    pattern = existing_stone.get_pattern(orientation)
    if pattern not in patterns:
        patterns.append(pattern)
    pattern.stones.append(stone)
    stone.patterns.append(pattern)


class BoardPattern(object):
    def __init__(self, board):
        self._black_stone_patterns = []
        self._white_stone_patterns = []
        self._board = board

    def add_stone(self, stone):
        patterns = self._black_stone_patterns if stone.color == StoneColor.black else self._white_stone_patterns
        if not self._check_existing_patterns(stone):
            patterns.append(Pattern(stone))
        self._update_patterns_end_free()
        self._sort_patterns()

    def _update_patterns_end_free(self):
        for pattern in self.white_stone_patterns + self.black_stone_patterns:
            if pattern.orientation != Orientation.any:
                min_stone_next_pos, max_stone_next_pos = pattern.end_stones_next_position(self._board)
                pattern.min_stone_free = pattern.min_stone_free and min_stone_next_pos is not None
                pattern.max_stone_free = pattern.max_stone_free and max_stone_next_pos is not None
                if pattern.min_stone_free:
                    min_row, min_col = min_stone_next_pos
                    pattern.min_stone_free = self._board.board_state[min_row][min_col] == 0
                if pattern.max_stone_free:
                    max_row, max_col = max_stone_next_pos
                    pattern.max_stone_free = self._board.board_state[max_row][max_col] == 0

    def _check_existing_patterns(self, stone):
        patterns = self._black_stone_patterns if stone.color == StoneColor.black else self._white_stone_patterns
        match_h = self._check_orientation(stone, Orientation.horizontal, [-1, 0], [1, 0], patterns)
        match_v = self._check_orientation(stone, Orientation.vertical, [0, 1], [0, -1], patterns)
        match_ld = self._check_orientation(stone, Orientation.left_diagonal, [-1, 1], [1, -1], patterns)
        match_rd = self._check_orientation(stone, Orientation.right_diagonal, [-1, -1], [1, 1], patterns)
        return match_h or match_v or match_ld or match_rd

    def _check_orientation(self, stone, orientation, o1, o2, patterns):
        color = stone.color
        row, col = stone.position
        o1_dr, o1_dc = o1
        o2_dr, o2_dc = o2
        o1_stone_is_same_color = self._check_dr_dc(color, row, col, o1_dr, o1_dc)
        o2_stone_is_same_color = self._check_dr_dc(color, row, col, o2_dr, o2_dc)
        found = True
        if o1_stone_is_same_color:
            o1_stone = self._board.board_stone[row + o1_dr][col + o1_dc]
            if o2_stone_is_same_color:
                o2_stone = self._board.board_stone[row + o2_dr][col + o2_dc]
                o1_pattern = o1_stone.get_pattern(orientation)
                # add o1_pattern if not in patterns, can happen if the o1_happen is newly created in get_pattern()
                if o1_pattern not in patterns:
                    patterns.append(o1_pattern)
                o2_pattern = o2_stone.get_pattern(orientation)
                o1_pattern.stones.append(stone)
                stone.patterns.append(o1_pattern)
                for stone in o2_pattern.stones:
                    # add stones form Orientation 2 to Orientation 1
                    o1_pattern.stones.append(stone)
                    # remove o2_pattern reference
                    stone.patterns.remove(o2_pattern)
                    stone.patterns.append(o1_pattern)
                if o2_pattern in patterns:
                    patterns.remove(o2_pattern)
            else:
                _update_pattern_along_orientation(o1_stone, orientation, stone, patterns)
        else:
            if o2_stone_is_same_color:
                o2_stone = self._board.board_stone[row + o2_dr][col + o2_dc]
                _update_pattern_along_orientation(o2_stone, orientation, stone, patterns)
            else:
                found = False
        return found

    def _check_dr_dc(self, color, row, col, dr, dc):
        row += dr
        col += dc
        if self._board.position_exist(row, col):
            stone = self._board.board_stone[row][col]
            if stone != 0 and stone.color == color:
                return True
            else:
                return False
        else:
            return False

    def _sort_patterns(self):
        self._black_stone_patterns.sort(reverse=True)
        self._white_stone_patterns.sort(reverse=True)

    def __repr__(self):
        rep = repr(self.black_stone_patterns)
        rep += "\n"
        rep += repr(self.white_stone_patterns)
        return rep

    @property
    def black_stone_patterns(self):
        return self._black_stone_patterns

    @property
    def white_stone_patterns(self):
        return self._white_stone_patterns

    @property
    def five_stones_found(self):
        if len(self._white_stone_patterns) == 0:
            return False
        else:
            if self._black_stone_patterns[0].number_of_stones >= 5 \
                    or self._white_stone_patterns[0].number_of_stones >= 5:
                return True
            else:
                return False
