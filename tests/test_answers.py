from contextlib import redirect_stdout
from io import StringIO

from aoc.__main__ import main

answers = {
    1: [2344935, 27647262],
    2: [213, 285]
}

def test_answers_correct():
    for day, puzzles in answers.items():
        for i, answer in enumerate(puzzles):
            f = StringIO()
            with redirect_stdout(f):
                main(day, i + 1)
            assert f.getvalue().strip() == str(answer), f"{day} {i}"
