import string
from typing import List, Tuple
import utils


def is_symbol(x: str):
    return x not in string.digits and x != "."


def found_adjacent_symbol(i: int, j: int, engine: List[str]) -> bool:
    for di in [-1, 0, 1]:
        for dj in [-1, 0, 1]:
            new_i, new_j = i + di, j + dj
            if (
                0 <= new_i
                and new_i < len(engine)
                and 0 <= new_j
                and new_j < len(engine[0])
                and is_symbol(engine[new_i][new_j])
            ):
                return True
    return False


def find_engine_numbers(engine: List[str]) -> List[int]:
    numbers = []
    for i, row in enumerate(engine):
        current_number, found_symbol = "", False
        for j, c in enumerate(row):
            if c in string.digits:
                current_number += c
                found_symbol |= found_adjacent_symbol(i, j, engine)
            else:
                if found_symbol and current_number:
                    numbers.append(int(current_number))
                current_number, found_symbol = "", False

        if found_symbol and current_number:
            numbers.append(int(current_number))

    return numbers


def get_number_and_positions(i, j, engine) -> Tuple[int, set]:
    number = engine[i][j]
    positions = set()

    start = j
    while start - 1 >= 0 and engine[i][start - 1] in string.digits:
        start -= 1
    end = j
    while end < len(engine[0]) and engine[i][end] in string.digits:
        end += 1

    return int(engine[i][start:end]), set([(i, x) for x in range(start, end)])


def find_adjacent_numbers(i, j, engine) -> List[int]:
    numbers = []
    seen_positions = set()
    for di in [-1, 0, 1]:
        for dj in [-1, 0, 1]:
            new_i, new_j = i + di, j + dj
            if (
                0 <= new_i
                and new_i < len(engine)
                and 0 <= new_j
                and new_j < len(engine[0])
                and engine[new_i][new_j] in string.digits
                and (new_i, new_j) not in seen_positions
            ):
                number, positions = get_number_and_positions(new_i, new_j, engine)
                numbers.append(number)
                seen_positions |= positions
    return numbers


def find_all_gear_ratios(engine: List[str]) -> List[int]:
    ratios = []
    for i, row in enumerate(engine):
        for j, c in enumerate(row):
            if is_symbol(c):
                numbers = find_adjacent_numbers(i, j, engine)
                if len(numbers) == 2:
                    ratios.append(numbers[0] * numbers[1])
    return ratios


FNAME = "engine.txt"
engine = utils.read_lines(FNAME)
numbers = find_engine_numbers(engine)
gear_ratios = find_all_gear_ratios(engine)
print(sum(gear_ratios))
