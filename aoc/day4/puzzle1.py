def check_horizontal(row: str, pos: int) -> bool:
    for k in range(3):
        if row[pos + k + 1] != "MAS"[k]:
            return False
    return True


def check_vertical(rows: list[str], pos: int) -> bool:
    for k in range(3):
        if rows[k][pos] != "MAS"[k]:
            return False
    return True


def check_diagonal(rows: list[str], pos: int) -> bool:
    for k in range(3):
        if rows[k][pos + k + 1] != "MAS"[k]:
            return False
    return True


def main(input: str) -> int:
    count = 0
    split = input.splitlines()
    for i, row in enumerate(split):
        for j, char in enumerate(row):
            if char != "X":
                continue

            # check our columns first so we can also pull the rows
            # above and below ours if we'll need them for diagonals
            next_rows = earlier_rows = None
            if i < len(split) - 3:
                next_rows = split[i + 1: i + 4]
                count += int(check_vertical(split[i + 1: i + 4], j))
            if i >= 3:
                stop = i - 4 if i != 3 else None
                earlier_rows = split[i - 1:stop:-1]
                count += int(check_vertical(earlier_rows, j))
    
            # check if we can have a forward horizontal
            if j < len(row) - 3:
                count += int(check_horizontal(row, j))
                # if we're not at the bottom, check if we can have either
                # of the left-to-right diagonals
                if next_rows is not None:
                    count += int(check_diagonal(next_rows, j))
                if earlier_rows is not None:
                    count += int(check_diagonal(earlier_rows, j))
    
            # now check if we can have a backward horizontal
            if j >= 3:
                k = len(row) - j - 1
                count += int(check_horizontal(row[::-1], k))

                # check any of the right-to-left diagonals
                if next_rows is not None:
                    count += int(check_diagonal([i[::-1] for i in next_rows], k))
                if earlier_rows is not None:
                    count += int(check_diagonal([i[::-1] for i in earlier_rows], k))
    return count
