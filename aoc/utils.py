import os
import requests
from collections.abc import Callable
from functools import cache, wraps
from typing import TypeVar

T = TypeVar("T")


@cache
def get_input(year: int, day: int) -> str:
    cookie = os.environ.get("AOC_COOKIE")
    if cookie is None:
        raise EnvironmentError("Must specify AOC_COOKIE environment variable")
    response = requests.get(
        f"https://adventofcode.com/{year}/day/{day}/input", cookies={"session": cookie}
    )
    response.raise_for_status()
    return response.content.decode()


def parse_input(
    preprocessor: Callable[[str], T]
) -> Callable[[Callable[[T], str | int]], Callable[[str], str | int]]:
    def wrapper(func: Callable[[T], str | int]) -> Callable[[str], str | int]:
        @wraps(func)
        def wrapped(input: str) -> None:
            result = preprocessor(input)
            if isinstance(result, tuple):
                return func(*result)
            return func(result)
        return wrapped
    return wrapper
