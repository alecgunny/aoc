import os
import requests
from functools import cache


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
