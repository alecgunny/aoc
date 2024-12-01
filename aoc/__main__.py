import importlib
from argparse import ArgumentParser
from typing import Callable

from aoc.client import get_input


def main(day: int, puzzle: int) -> None:
    module = importlib.import_module(f"aoc.day{day}")
    input = get_input(2024, day)
    func: Callable[[str], None] = getattr(module, f"puzzle{puzzle}")
    return func(input)


def cli(args: list[str] | None = None) -> None:
    parser = ArgumentParser(prog="Advent of Code")
    parser.add_argument("day", type=int)
    parser.add_argument("puzzle", type=int, choices=[1, 2])
    flags = parser.parse_args(args)
    return main(flags.day, flags.puzzle)


if __name__ == "__main__":
    cli()
