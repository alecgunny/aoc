import os
import requests
from collections.abc import Callable
from functools import cache, wraps
from typing import TypeVar

T = TypeVar("T")


def cache_response(func):
    cache_dir = ".cache"
    os.makedirs(cache_dir, exist_ok=True)
    cache_file = os.path.join(cache_dir, "{year}_{day}.txt")


@cache
def get_input(year: int, day: int) -> str:
    cache_dir = ".cache"
    cache_file = os.path.join(cache_dir, f"{year}_{day}.txt")
    if os.path.exists(cache_file):
        with open(cache_file, "r") as f:
            return f.read()

    cookie = os.environ.get("AOC_COOKIE")
    if cookie is None:
        raise EnvironmentError("Must specify AOC_COOKIE environment variable")
    response = requests.get(
        f"https://adventofcode.com/{year}/day/{day}/input", cookies={"session": cookie}
    )
    response.raise_for_status()
    input = response.content.decode()

    os.makedirs(cache_dir, exist_ok=True)
    with open(cache_file, "w") as f:
        f.write(input)
    return input


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
