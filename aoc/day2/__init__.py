__all__ = ["puzzle1", "puzzle2"]


def get_report(input: str) -> list[list[int]]:
    return [list(map(int, i.split())) for i in input.splitlines()]


def check_row(row: list[int]) -> bool:
    diffs = [j - i for i, j in zip(row[:-1], row[1:])]
    sign = diffs[0] > 0
    return all([1 <= abs(i) <= 3 for i in diffs]) and all([(i > 0) == sign for i in diffs])


def puzzle1(input: str) -> None:
    print(len(list(filter(check_row, get_report(input)))))


def puzzle2(input: str) -> None:
    count = 0
    for row in get_report(input):
        if check_row(row):
            count += 1
            continue
        for i in range(len(row)):
            if check_row(row[:i] + row[i + 1:]):
                count += 1
                break
    print(count)
