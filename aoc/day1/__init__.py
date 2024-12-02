from aoc.utils import parse_input

__all__ = ["puzzle1", "puzzle2"]


def get_lists(input: str) -> tuple[list[int], list[int]]:
    lists = zip(*[i.split() for i in input.strip().splitlines()])
    return tuple([list(map(int, i)) for i in lists])


@parse_input(get_lists)
def puzzle1(l1: list[int], l2: list[int]) -> int:
    return sum([abs(i - j) for i, j in zip(sorted(l1), sorted(l2))])


@parse_input(get_lists)
def puzzle2(l1: list[int], l2: list[int]) -> int:
    values = set(l1)
    return sum([i for i in l2 if i in values])
