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
        plt.text(x, y, str(self._step), size=16, color=color, ha="center", va="center", zorder=20)

    def get_pattern(self, orientation):
        pattern_any = 0
        for pattern in self.patterns:
            if pattern.orientation == orientation:
                return pattern
            elif pattern.orientation == Orientation.any:
                pattern_any = pattern
                break
        if pattern_any == 0:
            # TODO: Test
            pattern = Pattern(self)
        else:
            pattern = pattern_any
        pattern.orientation = orientation
        return pattern

    @property
    def position(self):
        return self._position

    @property
    def color(self):
        return self._color

    @property
    def step(self):
        return self._step


def _update_pattern_along_orientation(existing_stone, orientation, stone, patterns):
    pattern = existing_stone.get_pattern(orientation)
    if pattern not in patterns:
        patterns.append(pattern)
    pattern.stones.append(stone)
    stone.patterns.append(pattern)


class Orientation(enum.Enum):
    any = "any"
    horizontal = "horizontal"
    vertical = "vertical"
    left_diagonal = "left_diagonal"
    right_diagonal = "right_diagonal"


class Pattern(object):
    def __init__(self, stone):
        self._color = stone.color
        self.orientation = Orientation.any
        self.stones = [stone]

        stone.patterns.append(self)

    def __repr__(self):
        rep = "b " if self._color == StoneColor.black else "w "
        rep += str(self.number_of_stones) + " "
        rep += self.orientation.value + " "
        rep += "["
        for stone in self.stones:
            rep += str(stone.step) + " "
        rep = rep[:-1]
        rep += "]"
        return rep

    def __lt__(self, other):
        return self.number_of_stones < other.number_of_stones

    @property
    def color(self):
        return self._color

    @property
    def number_of_stones(self):
        return len(self.stones)


class BoardPattern(object):
    def __init__(self, board):
        self._black_stone_patterns = []
        self._white_stone_patterns = []
        self._board = board

    def add_stone(self, stone):
        patterns = self._black_stone_patterns if stone.color == StoneColor.black else self._white_stone_patterns
        if not self._check_existing_patterns(stone):
            patterns.append(Pattern(stone))
        self._sort_patterns()

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

    def _position_exist(self, row, col):
        return 0 < row < self._board.board_size and 0 < col < self._board.board_size

    def _check_dr_dc(self, color, row, col, dr, dc):
        row += dr
        col += dc
        if self._position_exist(row, col):
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

    @property
    def black_stone_patterns(self):
        return self._black_stone_patterns

    @property
    def white_stone_patterns(self):
        return self._white_stone_patterns

    @property
    def five_stones_found(self):
        if len(self._white_stone_patterns) == 0 :
            return False
        else:
            if self._black_stone_patterns[0].number_of_stones >= 5 \
                    or self._white_stone_patterns[0].number_of_stones >= 5:
                return True
            else:
                return False
