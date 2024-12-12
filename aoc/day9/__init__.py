from itertools import zip_longest

from aoc.utils import parse_input

def make_disk(image: list[int]) -> tuple[list[int], dict[int, int]]:
    disk: list[int] = []
    file_sizes: dict[int, int] = {}
    idx = 0
    for i, (file_size, open_size) in enumerate(zip_longest(image[::2], image[1::2])):
        if file_size is not None:
            file_sizes[i] = file_size
            disk.extend([i for _ in range(file_size)])
            idx += file_size

        if open_size is not None:
            disk.extend([-1 for _ in range(open_size)])
            idx += open_size
    return disk, file_sizes


def parse(input: str) -> list[int]:
    return make_disk(list(map(int, input.strip())))


@parse_input(parse)
def puzzle1(disk: list[int], file_sizes: dict[int, int]) -> int:
    backward_idx = len(disk) - 1
    forward_idx = file_sizes[0]
    while backward_idx > forward_idx:
        while disk[backward_idx] == -1:
            backward_idx -= 1
        file_id = disk[backward_idx]
        while disk[forward_idx] != -1:
            forward_idx += file_sizes[disk[forward_idx]]
        disk[forward_idx] = file_id
        disk[backward_idx] = -1

        forward_idx += 1
        backward_idx -= 1
    return sum([i * j for i, j in enumerate(disk) if j != -1])


@parse_input(parse)
def puzzle2(disk: list[int], file_sizes: dict[int, int]) -> int:
    files_attempted = set()
    backward_idx = len(disk) - 1
    while backward_idx > file_sizes[0]:
        while disk[backward_idx] == -1:
            backward_idx -= 1

        # check if we've already attempted to move this file,
        # and if so move our pointer back and keep going
        file_id = disk[backward_idx]
        file_size = file_sizes[file_id]
        if file_id in files_attempted:
            backward_idx -= file_size
            continue

        files_attempted.add(file_id)
        forward_idx = file_sizes[0]
        current_block_size = 0
        while forward_idx < backward_idx - file_size:
            # if we're in an open block, keep iterating through it until we either
            # hit our current file's size, or we enter another file
            while disk[forward_idx] == -1:
                current_block_size += 1
                forward_idx += 1
                if current_block_size == file_size:
                    break
            else:
                # we never broke, which means this space isn't big enough.
                # reset our current block size
                current_block_size = 0

                # while we're in a file, skip forward by the file's length
                # until we hit another open space or we skip over our current
                # file's position in the disk
                while disk[forward_idx] != -1:
                    if forward_idx >= backward_idx - file_size:
                        break
                    forward_idx += file_sizes[disk[forward_idx]]
                else:
                    # we didn't break, which means we ended the loop by entering
                    # another open space
                    continue

                # otherwise, we broke which means we passed our
                # current file and can stop searching
                break

            # only got here if we broke the loop above, which means we
            # found a spot for our file, so fill out our last file_size
            # spots in the disk and delete the spots it used to occupy
            for i in range(file_size):
                disk[forward_idx - i - 1] = file_id
                disk[backward_idx - i] = -1
            break

        # whether we moved the file or not, move our disk index back
        backward_idx -= file_size
    return sum([i * j for i, j in enumerate(disk) if j != -1])