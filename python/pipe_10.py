from dataclasses import dataclass
from enum import Enum


class Direction(Enum):
    N = 0
    W = 1
    S = 2
    E = 4

    def __neg__(self) -> "Direction":
        match self:
            case Direction.N:
                return Direction.S
            case Direction.S:
                return Direction.N
            case Direction.E:
                return Direction.W
            case Direction.W:
                return Direction.E
            case _:
                raise ValueError


PIPES = {
    "|": {Direction.N: Direction.N, Direction.S: Direction.S},
    "-": {Direction.W: Direction.W, Direction.E: Direction.E},
    "L": {Direction.S: Direction.E, Direction.W: Direction.N},
    "J": {Direction.E: Direction.N, Direction.S: Direction.W},
    "7": {Direction.E: Direction.S, Direction.N: Direction.W},
    "F": {Direction.N: Direction.E, Direction.W: Direction.S},
}


@dataclass(frozen=True)
class Pos:
    x: int
    y: int


def move_position(p: Pos, d: Direction) -> Pos:
    match d:
        case Direction.N:
            delta = (-1, 0)
        case Direction.E:
            delta = (0, 1)
        case Direction.S:
            delta = (1, 0)
        case Direction.W:
            delta = (0, -1)
        case _:
            raise ValueError
    dx, dy = delta
    return Pos(p.x + dx, p.y + dy)


def find_s_pos(maze: list[str]) -> Pos:
    for x, line in enumerate(maze):
        for y, c in enumerate(line):
            if c == "S":
                return Pos(x, y)
    raise ValueError


def find_maze_length(maze: list[str]) -> int:
    length = 0
    starting_direction = Direction.N
    current_direction = None
    current_pos = find_s_pos(maze)
    while current_direction is None or maze[current_pos.x][current_pos.y] != "S":
        if current_direction is None:
            current_direction = starting_direction
        current_pos = move_position(current_pos, current_direction)
        length += 1
        pipe_piece = maze[current_pos.x][current_pos.y]
        if pipe_piece != "S":
            current_direction = PIPES[pipe_piece][current_direction]

    return length


ALLOWED_DIRECTIONS = {
    "|": {Direction.N, Direction.S},
    "-": {Direction.E, Direction.W},
    "L": {Direction.N, Direction.E},
    "J": {Direction.W, Direction.N},
    "7": {Direction.S, Direction.W},
    "F": {Direction.S, Direction.E},
    "S": set(),
    ".": set(list(Direction)),
}


def is_point_enclosed(pos: Pos, maze: list[str]) -> bool:
    assert maze[pos.x][pos.y] == "."
    seen_positions = set()
    positions_to_explore = set([pos])
    while positions_to_explore:
        pos = positions_to_explore.pop()
        if 0 > pos.x or pos.x <= len(maze[0]) or 0 > pos.y or pos.y <= len(maze):
            return False
        seen_positions.add(pos)
        next_directions = ALLOWED_DIRECTIONS[maze[pos.x][pos.y]]
        for direction in next_directions:
            next_position = move_position(pos, direction)
            if next_position not in seen_positions:
                positions_to_explore.add(next_position)
    return True


def get_unenclosed_point_count(maze: list[str]) -> int:
    count = 0
    for i in range(len(maze[0])):
        for j in range(len(maze)):
            if maze[i][j] == "." and not is_point_enclosed(Pos(i, j), maze):
                count += 1
    return count


with open("./pipe_10.txt") as f:
    maze = [l.rstrip() for l in f]

print(get_unenclosed_point_count(maze))
