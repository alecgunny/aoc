from aoc.utils import parse_input

__all__ = ["puzzle1", "puzzle2"]


def get_report(input: str) -> list[list[int]]:
    return [list(map(int, i.split())) for i in input.splitlines()]


def check_row(row: list[int]) -> bool:
    diffs = [j - i for i, j in zip(row[:-1], row[1:])]
    sign = diffs[0] > 0
    return all([1 <= abs(i) <= 3 for i in diffs]) and all([(i > 0) == sign for i in diffs])


@parse_input(get_report)
def puzzle1(report: list[list[int]]) -> int:
    return len(list(filter(check_row, report)))


@parse_input(get_report)
def puzzle2(report: list[list[int]]) -> int:
    count = 0
    for row in report:
        if check_row(row):
            count += 1
            continue
        for i in range(len(row)):
            if check_row(row[:i] + row[i + 1:]):
                count += 1
                break
    return count
