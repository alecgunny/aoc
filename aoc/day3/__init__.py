import re


def puzzle1(input: str) -> int:
    pattern = re.compile("mul\(([1-9][0-9]{0,2}),([1-9][0-9]{0,2})\)")
    return sum([int(i[0]) * int(i[1]) for i in pattern.findall(input)])


def puzzle2(input: str) -> int:
    first_block, remainder = input.split("don't()", maxsplit=1)
    do_pattern = re.compile("do\(\).*?don't\(\)", flags=re.DOTALL)
    output = puzzle1(first_block) + sum(map(puzzle1, do_pattern.findall(remainder)))

    last_block = remainder.rsplit("do()", maxsplit=1)[-1]
    if "don't()" not in last_block:
        output += puzzle1(last_block)
    return output
