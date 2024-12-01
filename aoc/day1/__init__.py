__all__ = ["puzzle1", "puzzle2"]


def get_lists(input: str) -> tuple[list[int], list[int]]:
    lists = zip(*[i.split() for i in input.strip().splitlines()])
    return tuple([sorted(map(int, i)) for i in lists])


def puzzle1(input: str) -> None:
    l1, l2 = get_lists(input)
    print(sum([abs(i - j) for i, j in zip(l1, l2)]))


def puzzle2(input: str) -> None:
    l1, l2 = get_lists(input)
    values = set(l1)
    print(sum([i for i in l2 if i in values]))
