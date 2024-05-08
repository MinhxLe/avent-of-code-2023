import string
import utils

FILE_NAME = "./day1.txt"


def read_lines(fname):
    with open(fname) as file:
        lines = [line.rstrip() for line in file]
    return lines


def get_calibration_value(line: str) -> int:
    first_digit, last_digit = None, None
    for c in line:
        if c in string.digits:
            first_digit = c

    for c in reversed(line):
        if c in string.digits:
            last_digit = c
    assert first_digit is not None
    assert last_digit is not None
    return int(first_digit + last_digit)


lines = utils.read_lines(FILE_NAME)
values = [get_calibration_value(l) for l in lines]
