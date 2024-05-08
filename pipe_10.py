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


@dataclass
class Pipe:
    direction1: Direction
    direction2: Direction

    def map(self, direction: Direction) -> Direction:
        match -direction:
            case self.direction1:
                return self.direction2
            case self.direction2:
                return self.direction1
            case _:
                raise ValueError


PIPES = {
    "|": Pipe(Direction.S, Direction.N),
    "-": Pipe(Direction.W, Direction.E),
    "L": Pipe(Direction.N, Direction.E),
    "J": Pipe(Direction.N, Direction.W),
    "7": Pipe(Direction.S, Direction.E),
    "F": Pipe(Direction.S, Direction.E),
}


@dataclass
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
        print(f"{current_direction} {current_pos}")
        if current_direction is None:
            current_direction = starting_direction
        else:
            pipe_piece = maze[current_pos.x][current_pos.y]
            print(f"{pipe_piece} {current_direction}")
            current_direction = PIPES[pipe_piece].map(current_direction)
        current_pos = move_position(current_pos, current_direction)
        length += 1

    return length


with open("./pipe_10.txt") as f:
    maze = [l.rstrip() for l in f]

find_maze_length(maze)
