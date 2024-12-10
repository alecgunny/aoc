from collections import defaultdict
from aoc.utils import parse_input


def parse(input: str) -> tuple[dict[int, list[int]], list[list[int]]]:
    top, bottom = input.split("\n\n")
    rules: dict[int, list[int]] = defaultdict(list)
    for row in top.strip().splitlines():
        first, second = map(int, row.split("|"))
        rules[first].append(second)
    return rules, [list(map(int, i.split(","))) for i in bottom.strip().splitlines()]


def separate_updates(
    rules: dict[int, list[int]], updates: list[list[int]]
) -> tuple[list[list[int]], list[list[int]]]:
    good_updates, bad_updates = [], []
    for update in updates:
        for i, page in enumerate(update[-1:0:-1]):
            try:
                rule = rules[page]
            except KeyError:
                continue
            if any(j in rule for j in update[:-i - 1]):
                bad_updates.append(update)
                break
        else:
            good_updates.append(update)
    return good_updates, bad_updates


@parse_input(parse)
def puzzle1(rules: dict[int, list[int]], updates: list[list[int]]) -> int:
    good_updates, _ = separate_updates(rules, updates)
    return sum([i[int(len(i) // 2)] for i in good_updates])


@parse_input(parse)
def puzzle2(rules: dict[int, list[int]], updates: list[list[int]]) -> int:
    _, bad_updates = separate_updates(rules, updates)
    output = 0
    for update in bad_updates:
        correct_order = []
        remainder = set(update) - set(correct_order)
        while remainder:
            for page in remainder:
                for other in set(update) - set(correct_order) - set([page]):
                    try:
                        rule = rules[other]
                    except KeyError:
                        continue
                    if page in rule:
                        break
                else:
                    correct_order.append(page)
            remainder = set(update) - set(correct_order)
        output += correct_order[int(len(update) // 2)]
    return output