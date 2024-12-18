import importlib
from argparse import ArgumentParser
from typing import Callable

from aoc.utils import get_input


def main(day: int, puzzle: int) -> None:
    module = importlib.import_module(f"aoc.day{day}")
    input = get_input(2024, day)
    func: Callable[[str], str | int] = getattr(module, f"puzzle{puzzle}")
    result = func(input)
    print(result)


def cli(args: list[str] | None = None) -> None:
    parser = ArgumentParser(prog="Advent of Code")
    parser.add_argument("day", type=int, help="Day of the advent calendar to solve")
    parser.add_argument("puzzle", type=int, choices=[1, 2], help="Which of the two daily puzzles to solve")
    flags = parser.parse_args(args)
    main(flags.day, flags.puzzle)


if __name__ == "__main__":
    cli()
