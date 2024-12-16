from functools import wraps
from typing import Callable, Literal, NamedTuple

from aoc.utils import parse_input

Direction = Literal["<", ">", "^", "V"]

class Position(NamedTuple):
    x: int
    y: int

    def move(self, direction: Direction) -> "Position":
        if direction == "<":
            return Position(self.x - 1, self.y)
        elif direction == ">":
            return Position(self.x + 1, self.y)
        elif direction == "^":
            return Position(self.x, self.y - 1)
        else:
            return Position(self.x, self.y + 1)


class WideBox(NamedTuple):
    left: Position
    right: Position

    @classmethod
    def from_position(cls, position: Position, warehouse: "Warehouse") -> "WideBox":
        character = warehouse[position]
        if character not in "[]":
            raise ValueError(f"Instantiating WideBox from character {character}")

        if character == "[":
            box = cls(position, position.move(">"))
        else:
            box = cls(position.move("<"), position)
        return box

    def can_move(self, warehouse: "Warehouse", direction: Direction) -> bool:
        """
        Check if this box can can be moved in the indicated direction
        or if there's a wall in the way
        """
        if direction == "<":
            return not warehouse[self.left.move(direction)] == "#"
        elif direction == ">":
            return not warehouse[self.right.move(direction)] == "#"
        else:
            # for vertical motion, check if there's a wall in the way
            # of either the left or right edges of the box
            for position in self:
                if warehouse[position.move(direction)] == "#":
                    return False
            return True

    def move(self, direction: Direction) -> "WideBox":
        return WideBox(self.left.move(direction), self.right.move(direction))


def move_robot(func: Callable[[Direction], Position | None]) -> Callable[[Direction], None]:
    """
    Quick wrapper function to update our robot position as we make moves
    and keep track of it with an @ for debugging purposes.
    """
    def wrapper(self: "Warehouse", direction: Direction) -> None:
        new_position = func(self, direction)
        if new_position is not None:
            self[self.robot] = "."
            self.robot = new_position
            self[self.robot] = "@"
    return wrapper


class Warehouse:
    def __init__(self, grid: list[list[str]]) -> None:
        self.map = grid
        self.robot = next(i for i, j in self if j == "@")
        self._score_character = "O"

    def __getitem__(self, index: int | Position) -> str | list[str]:
        if isinstance(index, Position):
            return self.map[index.y][index.x]
        return self.map[index]

    def __setitem__(self, index: Position, value: str) -> None:
        if self[index] == "#":
            raise IndexError(f"Attempting to set a wall at position {index}")
        self.map[index.y][index.x] = value

    def __iter__(self):
        for y, row in enumerate(self.map):
            for x, character in enumerate(row):
                yield Position(x, y), character

    def move_boxes(self, next_position: Position, direction: Direction) -> Position | None:
        # find all the boxes we have stacked against one another
        robot_position = next_position
        while self[next_position] == "O":
            next_position = next_position.move(direction)
            if self[next_position] == "#":
                # the last box is backed against a wall, so we can't move
                return

        # move the last box into the next position, then return the next
        # position of the robot (which will "move" the first box)
        self[next_position] = "O"
        return robot_position

    @move_robot
    def move(self, direction: Direction) -> Position | None:
        """
        Return the next position if we're moving, return None otherwise
        """

        next_position = self.robot.move(direction)
        if self[next_position] == "#":
            # if our next position is blocked, don't do anything
            return
        if self[next_position] == ".":
            # if it's empty, just move there and exit
            return next_position
        return self.move_boxes(next_position, direction)

    def score(self) -> int:
        return sum([100 * i.y + i.x for i, j in self if j == self._score_character])

    def __str__(self) -> str:
        return "\n".join(["".join(i) for i in self.map])


class WideWarehouse(Warehouse):
    def __init__(self, grid: list[list[str]]) -> None:
        wide_map: list[list[str]] = []
        for row in grid:
            wide_row = []
            for character in row:
                if character in ".#":
                    wide_row.extend(character * 2)
                elif character == "O":
                    wide_row.extend("[]")
                elif character == "@":
                    wide_row.extend("@.")
            wide_map.append(wide_row)

        super().__init__(wide_map)
        self._score_character = "["

    def move_boxes(self, next_position: Position, direction: Direction) -> Position | None:

        def find_attached_boxes(box: WideBox) -> list[WideBox]:
            """
            Recursively find all the boxes attached to the given box
            along the current direction.
            """
            if direction == ">" and self[box.right.move(">")] == "[":
                next_boxes = [WideBox.from_position(box.right.move(">"), self)]
            elif direction == "<" and self[box.left.move("<")] == "]":
                next_boxes = [WideBox.from_position(box.left.move("<"), self)]
            elif direction in "^v":
                # for vertical movement, we need to find all (unique) boxes
                # that are attached to either edge of the current box
                next_boxes = []
                for position in box:
                    next_position = position.move(direction)
                    character = self[next_position]
                    if character in "[]":
                        next_boxes.append(WideBox.from_position(next_position, self))
                next_boxes = list(set(next_boxes))
            else:
                return []

            all_boxes = next_boxes + [i for box in next_boxes for i in find_attached_boxes(box)]
            return list(set(all_boxes))

        # find all the boxes attached in a chain to the box
        # in the next position along the current dimension
        box = WideBox.from_position(next_position, self)
        boxes: list[WideBox] = [box] + find_attached_boxes(box)
        if not all([i.can_move(self, direction) for i in boxes]):
            return

        # move the boxes and update our grid according to the new positions
        moved_boxes = [i.move(direction) for i in boxes]
        for box in moved_boxes:
            for position, character in zip(box, "[]"):
                self[position] = character

        # reset any positions that are now empty after a box moved
        positions = set([i for j in boxes for i in j]) - set([i for j in moved_boxes for i in j])
        for position in positions:
            self[position] = "."
        return next_position


def get_map_and_sequence(input: str) -> tuple[list[list[str]], str]:
    grid, sequence = input.strip().split("\n\n")
    return list(map(list, grid.splitlines())), sequence.replace("\n", "")


@parse_input(get_map_and_sequence)
def puzzle1(grid: list[list[str]], sequence: str) -> int:
    warehouse = Warehouse(grid)
    for step in sequence:
        warehouse.move(step)
    return warehouse.score()


@parse_input(get_map_and_sequence)
def puzzle2(grid: list[list[str]], sequence: str) -> int:
    warehouse = WideWarehouse(grid)
    for step in sequence:
        warehouse.move(step)
    return warehouse.score()