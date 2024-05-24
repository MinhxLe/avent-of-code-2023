from dish_14 import calculate_load_for_group, spin_platform, tilt_platform, Direction
import numpy as np


def test_calculate_load_for_group():
    # |o..
    assert calculate_load_for_group(-1, 3, 1) == 3
    # |oo.
    assert calculate_load_for_group(-1, 3, 2) == 5

    # |#oo
    assert calculate_load_for_group(0, 3, 2) == 3
    # |##ooo.
    assert calculate_load_for_group(1, 6, 3) == 9


def P(platform: str) -> np.ndarray:
    return np.array([list(s) for s in platform.strip().split("\n")])


def test_tilt_platform():
    assert (tilt_platform(P("#..O"), Direction.W) == P("#O..")).all()
    assert (tilt_platform(P("#..O.O"), Direction.W) == P("#OO...")).all()
    assert (tilt_platform(P("#..O#O"), Direction.W) == P("#O..#O")).all()
    assert (tilt_platform(P("O..#"), Direction.E) == P("..O#")).all()
    assert (tilt_platform(P("#\n.\n.\nO"), Direction.N) == P("#\nO\n.\n.")).all()
    assert (tilt_platform(P("O\n.\n.\n#"), Direction.S) == P(".\n.\nO\n#")).all()


def test_spin_platform():
    assert (spin_platform(P(".O.\n...\n..."), 1) == P("...\n...\n..O")).all()
    start = """
.#.
.O.
...
"""
    end = """
.#.
...
..O
"""
    assert (spin_platform(P(start), 1000000000) == P(end)).all()


def test_spin_platform_2():
    start = """
.#.O
..O.
..#.
"""

    end = """
.#.O
....
.O#.
"""
    print(spin_platform(P(start), 10))
