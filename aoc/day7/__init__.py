import operator
from collections.abc import Callable
from itertools import product

from aoc.utils import parse_input

Operator = Callable[[int, int], int]
Equations = list[tuple[int, list[int]]]


def parse(input: str) -> Equations:
    lines = [i.split(":") for i in input.strip().splitlines()]
    return [(int(i), list(map(int, j.split()))) for i, j in lines]


def concat(a: int, b: int) -> int:
    return a * 10**(len(str(b))) + b


def check_ops(target: int, inputs: list[int], ops: list[Operator]) -> bool:
    value = inputs[0]
    for i, op in enumerate(ops):
        value = op(value, inputs[i + 1])
    return value == target


def check_equation(target: int, inputs: list[int], ops: list[Operator]) -> bool:
    for ops in product(ops, repeat=len(inputs) - 1):
        if check_ops(target, inputs, ops):
            return True
    return False


def solve(equations: Equations, include_concat: bool = False) -> int:
    muladd = [operator.mul, operator.add]
    output = 0
    for target, inputs in equations:
        if check_equation(target, inputs, [operator.mul, operator.add]):
            output += target
        elif include_concat and check_equation(target, inputs, muladd + [concat]):
            output += target
    return output


@parse_input(parse)
def puzzle1(equations: Equations) -> int:
    return solve(equations, False)


@parse_input(parse)
def puzzle2(equations: Equations) -> int:
    return solve(equations, True)
