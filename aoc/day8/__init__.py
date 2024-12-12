from math import gcd
from collections import defaultdict
from itertools import combinations

from aoc.utils import parse_input


def parse(input: str) -> list[list[str]]:
    return [list(i) for i in input.strip().splitlines()]


def sign(x: int) -> int:
    if x == 0:
        return 0
    return abs(x) / x


def count_antinodes(grid: list[list[int]], max_steps: int | None = None) -> None:
    height = len(grid)
    width = len(grid[0])

    frequency_map: dict[str, list[tuple[int, int]]] = defaultdict(list)
    for i, row in enumerate(grid):
        for j, frequency in enumerate(row):
            if frequency != ".":
                frequency_map[frequency].append((j, i))

    for frequency, indices in frequency_map.items():
        for towers in combinations(indices, 2):
            diffs = [i - j for i, j in zip(*towers)]

            # if we don't care about distance, figure out what
            # the minimum step size is to be on the line connecting
            # the two towers
            if max_steps is None:
                denom = gcd(*diffs)
                diffs = [int(i / denom) for i in diffs]

            for i, tower in enumerate(towers):
                direction = (-1)**(i + 1)
                step = 0
                while step < (max_steps or float("inf")):
                    x, y = [i - direction * (step + 1) * diff for i, diff in zip(tower, diffs)]
                    if x < 0 or y < 0 or x >= width or y >= height:
                        break
                    grid[y][x] = "#"
                    step += 1

                if max_steps is not None:
                    continue

                step = 0
                while True:
                    x, y = [i + direction * (step + 1) * diff for i, diff in zip(tower, diffs)]
                    xt, _ = towers[1 - i]
                    if xt == x:
                        grid[y][x] = "#"
                        break
                    grid[y][x] = "#"
                    step += 1
    return "\n".join(["".join(i) for i in grid]).count("#")


@parse_input(parse)
def puzzle1(grid: list[list[int]]) -> int:
    return count_antinodes(grid, 1)


@parse_input(parse)
def puzzle2(grid: list[list[int]]) -> int:
    return count_antinodes(grid)