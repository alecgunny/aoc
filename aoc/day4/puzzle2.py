def check_forward_diag(above: str, below: str, pos: int) -> bool:
    for char1, char2 in ["MS", "SM"]:
        if above[pos - 1] == char1 and below[pos + 1] == char2:
            return True


def check_backward_diag(above: str, below: str, pos: int) -> bool:
    for char1, char2 in ["MS", "SM"]:
        if above[pos + 1] == char1 and below[pos - 1] == char2:
            return True


def main(input: str) -> int:
    count = 0
    split = input.splitlines()
    for i, row in enumerate(split[1:-1]):
        for j, char in enumerate(row[1:-1]):
            if char != "A":
                continue
            above, below = split[i:i + 3:2]
            if (
                check_forward_diag(above, below, j + 1)
                and check_backward_diag(above, below, j + 1)
            ):
                count += 1
    return count
