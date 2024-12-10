from copy import deepcopy
from typing import NamedTuple, Literal, Union

from tqdm import trange

from aoc.utils import parse_input

Direction = Literal["^", "V", ">", "<"]


class Grid:
    def __init__(self, grid: list[list[str]]) -> None:
        self._grid = grid
        self.position = Point.from_grid(self)

    def __getitem__(self, idx: Union[int, "Point"]) -> str | list[str]:
        if isinstance(idx, Point):
            return self._grid[idx.y][idx.x]
        return self._grid[idx]

    def __setitem__(self, idx: "Point", value: str) -> None:
        self._grid[idx.y][idx.x] = value

    def __len__(self) -> int:
        return len(self._grid)

    def __iter__(self):
        return iter(self._grid)

    def __contains__(self, point: "Point") -> bool:
        return 0 <= point.x < len(self[0]) and 0 <= point.y < len(self)

    @property
    def solved(self) -> bool:
        return self.position is None

    def update(self) -> None:
        self[self.position] = "X"

    def move(self) -> "Point":
        next_position = self.position.increment()
        if not next_position in self:
            self.update()
            self.position = None
        elif self[next_position] == "#":
            self.position = self.position.turn()
        else:
            self.update()
            self.position = next_position

    def solve(self) -> str | None:
        direction_grid = [[set() for _ in range(len(self[0]))] for _ in range(len(self))]
        while not self.solved:
            # if we ended up in the same spot travelling the same direction,
            # we're in a loop, so break here
            directions = direction_grid[self.position.x][self.position.y]
            if self.position.direction in directions:
                return None

            # otherwise record the direction at this grid location and keep moving
            directions.add(self.position.direction)
            self.move()
        return "\n".join(["".join(i) for i in self])


class Point(NamedTuple):
    x: int
    y: int
    direction: Direction

    @classmethod
    def from_grid(cls, grid: Grid) -> "Point":
        direction: str
        for y, row in enumerate(grid):
            for direction in "^V<>":
                try:
                    x = row.index(direction)
                except ValueError:
                    continue
                break
            else:
                continue
            break

        return cls(x, y, direction)

    def increment(self) -> "Point":
        if self.direction == "^":
            return Point(self.x, self.y - 1, self.direction)
        elif self.direction == ">":
            return Point(self.x + 1, self.y, self.direction)
        elif self.direction == "V":
            return Point(self.x, self.y + 1, self.direction)
        elif self.direction == "<":
            return Point(self.x - 1, self.y, self.direction)

    def turn(self) -> "Point":
        if self.direction == "^":
            return Point(self.x, self.y, ">")
        elif self.direction == ">":
            return Point(self.x, self.y, "V")
        elif self.direction == "V":
            return Point(self.x, self.y, "<")
        elif self.direction == "<":
            return Point(self.x, self.y, "^")


def parse(input: str) -> list[str]:
    return Grid(list(map(list, input.strip().splitlines())))


@parse_input(parse)
def puzzle1(grid: Grid) -> int:
    return grid.solve().count("X")


@parse_input(parse)
def puzzle2(grid: Grid) -> int:
    # Trick here is that we only need to check for positions
    # that we would have run into in the original grid, so start
    # by solving the original grid, and then just check for the
    # positions that have X's
    solved_grid = deepcopy(grid)
    solved_grid.solve()

    loops = 0
    for i in trange(len(grid)):
        for j in range(len(grid[0])):
            if not (grid[i][j] == "." and solved_grid[i][j] == "X"):
                continue
            grid_ij = deepcopy(grid)
            grid_ij[i][j] = "#"
            if grid_ij.solve() is None:
                loops += 1
    return loops
