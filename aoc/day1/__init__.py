__all__ = ["puzzle1", "puzzle2"]


def get_lists(input: str) -> tuple[list[int], list[int]]:
    lists = zip(*[(j for j in i.split() if j) for i in input.splitlines() if i])
    return tuple([sorted(map(int, i)) for i in lists])


def puzzle1(input: str) -> None:
    l1, l2 = get_lists(input)
    print(sum([abs(i - j) for i, j in zip(l1, l2)]))


def puzzle2(input: str) -> None:
    l1, l2 = get_lists(input)
    counts = {v: 0 for v in l1}
    for value in l2:
        try:
            counts[value] += 1
        except KeyError:
            continue
    print(sum([k * v for k, v in counts.items()]))
