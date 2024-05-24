import string
import utils

FILE_NAME = "./day1.txt"


def read_lines(fname):
    with open(fname) as file:
        lines = [line.rstrip() for line in file]
    return lines


def find_first_digit(line: str, reverse=False) -> str:
    str_to_int_map = dict(
        one="1",
        two="2",
        three="3",
        four="4",
        five="5",
        six="6",
        seven="7",
        eight="8",
        nine="9",
    )

    if reverse:
        line = "".join(reversed(line))
        str_to_int_map = {"".join(reversed(k)): v for k, v in str_to_int_map.items()}

    for i, c in enumerate(line):
        if c in string.digits:
            return c
        else:
            for key, val in str_to_int_map.items():
                if key in line[: i + 1]:
                    return val


def get_calibration_value(line: str) -> int:
    first_digit = find_first_digit(line, reverse=False)
    last_digit = find_first_digit(line, reverse=True)
    print(line, first_digit + last_digit)
    assert first_digit is not None
    assert last_digit is not None
    return int(first_digit + last_digit)


lines = utils.read_lines(FILE_NAME)
values = [get_calibration_value(l) for l in lines]
print(sum(values))
