Solutions to Advent of Code puzzles.
Only supporting 2024 right now, but easy to generalize to any year with some light restructuring.

# Quick start
First follow [these instructions](https://github.com/jonathanpaulson/AdventOfCode/blob/8b7f4937ac5517ae3699d20702044c15a7faed22/get_input.py#L12C1-L16C45) and set your `AOC_COOKIE` environment variable to this value.

```console
export AOC_COOKIE=<session cookie>
```

All instructions here assume you have [Poetry](https://python-poetry.org/) installed.
Technically, all of this would be pip installable with `python -m pip install -e .`, but I won't document that route here.

```console
python -m poetry install
```

Then to see command line options you can run

```console
poetry run aoc --help                                                                                                                   ─╯
usage: Advent of Code [-h] day {1,2}

positional arguments:
  day         Day of the advent calendar to solve
  {1,2}       Which of the two daily puzzles to solve

options:
  -h, --help  show this help message and exit
```

So e.g. you could run

```console
poetry run python aoc 1 1
```

to solve the first puzzle from the first day of the calendar.