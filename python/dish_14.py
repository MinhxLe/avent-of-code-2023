from enum import Enum
import copy
import enum
import numpy as np


def calculate_load_for_group(row, num_rows, num_rocks):
    # if the rock group started at bottom row it would have 1+2+3... load
    load = (num_rocks * (num_rocks + 1)) // 2
    # every rock has the same offset load up based on row
    last_rock_row = row + num_rocks
    load += (num_rows - 1 - last_rock_row) * num_rocks
    return load


def calculate_load(platform: np.ndarray) -> int:
    M, N = platform.shape
    load = 0
    for col in range(N):
        cube_rock_row = -1
        num_rocks = 0
        for row in range(M):
            match platform[row, col]:
                case "#":
                    load += calculate_load_for_group(
                        cube_rock_row,
                        M,
                        num_rocks,
                    )
                    cube_rock_row = row
                    num_rocks = 0
                case "O":
                    num_rocks += 1
                case ".":
                    pass
                case _:
                    raise NotImplementedError

        if num_rocks > 0:
            load += calculate_load_for_group(
                cube_rock_row,
                M,
                num_rocks,
            )
    return load


class Symbol:
    DOT = "."
    HASH = "#"
    ROCK = "O"


class Direction(Enum):
    N = 0
    W = 1
    S = 2
    E = 4


def move_rocks(
    platform: np.ndarray,
    hash_idx: tuple[int, int],
    num_rocks: int,
    direction: Direction,
):
    match direction:
        case Direction.N:
            dx, dy = 1, 0
        case Direction.S:
            dx, dy = -1, 0
        case Direction.W:
            dx, dy = 0, 1
        case Direction.E:
            dx, dy = 0, -1
    x, y = hash_idx
    for _ in range(num_rocks):
        x, y = x + dx, y + dy
        platform[x, y] = Symbol.ROCK
    return platform


def tilt_platform(platform: np.ndarray, direction: Direction) -> np.ndarray:
    platform = platform.copy()
    X, Y = platform.shape
    match direction:
        case Direction.N:
            for j in range(Y):
                hash_idx = -1
                num_rocks = 0
                for i in range(X):
                    match platform[i, j]:
                        case Symbol.HASH:
                            move_rocks(platform, (hash_idx, j), num_rocks, direction)
                            num_rocks = 0
                            hash_idx = i
                        case Symbol.ROCK:
                            num_rocks += 1
                            platform[i, j] = Symbol.DOT
                if num_rocks > 0:
                    move_rocks(platform, (hash_idx, j), num_rocks, direction)

        case Direction.S:
            for j in range(Y):
                hash_idx = X
                num_rocks = 0
                for i in reversed(range(X)):
                    match platform[i, j]:
                        case Symbol.HASH:
                            move_rocks(platform, (hash_idx, j), num_rocks, direction)
                            num_rocks = 0
                            hash_idx = i
                        case Symbol.ROCK:
                            num_rocks += 1
                            platform[i, j] = Symbol.DOT
                if num_rocks > 0:
                    move_rocks(platform, (hash_idx, j), num_rocks, direction)
        case Direction.W:
            for i in range(X):
                hash_idx = -1
                num_rocks = 0
                for j in range(Y):
                    match platform[i, j]:
                        case Symbol.HASH:
                            move_rocks(platform, (i, hash_idx), num_rocks, direction)
                            num_rocks = 0
                            hash_idx = j
                        case Symbol.ROCK:
                            num_rocks += 1
                            platform[i, j] = Symbol.DOT
                if num_rocks > 0:
                    move_rocks(platform, (i, hash_idx), num_rocks, direction)
        case Direction.E:
            for i in range(X):
                hash_idx = Y
                num_rocks = 0
                for j in reversed(range(Y)):
                    match platform[i, j]:
                        case Symbol.HASH:
                            move_rocks(platform, (i, hash_idx), num_rocks, direction)
                            num_rocks = 0
                            hash_idx = j
                        case Symbol.ROCK:
                            num_rocks += 1
                            platform[i, j] = Symbol.DOT
                if num_rocks > 0:
                    move_rocks(platform, (i, hash_idx), num_rocks, direction)
    return platform


with open("./dish_14.txt") as f:
    platform = [list(line.rstrip()) for line in f]
platform = np.array(platform)
# part 1
print(calculate_load(platform))


def spin_platform(platform: np.ndarray, n: int) -> np.ndarray:
    repeat_idx = None
    platforms = [platform]
    for i in range(n):
        for direction in [Direction.N, Direction.W, Direction.S, Direction.E]:
            platform = tilt_platform(platform, direction)
        for j, p in enumerate(platforms):
            if (p == platform).all():
                repeat_idx = j
        if repeat_idx is None:
            platforms.append(platform)
        else:
            break
    if repeat_idx is None:
        return platform
    else:
        num_platforms = len(platforms)
        start_len = repeat_idx
        repeat_len = num_platforms - start_len
        offset = (n - start_len) % repeat_len
        return platforms[repeat_idx + offset]


# part2
NUM_ROTATIONS = 1_000_000_000
final_platform = spin_platform(platform, NUM_ROTATIONS)
print(calculate_load(final_platform))


"""
0 1 2 [3, 4 5] 3

start_len = repeat_idx+1
repeat_len = len - repeat_idx


final_idx = (NUM_ROTATIONS - start_len) % repeat_len
"""
