from typing_extensions import is_protocol
from galaxy_11 import calculate_distance, l1, parse_universe, P


def test_add_row():
    universe = [
        "#..",
        "..#",
    ]
    result = parse_universe(universe)
    assert result == [
        P(0, 0),
        P(1, 3),
    ]


def test_add_col():
    universe = [
        "#.",
        "..",
        ".#",
    ]
    result = parse_universe(universe)
    assert result == [
        P(0, 0),
        P(3, 1),
    ]


def test_add_both():
    universe = [
        "#..",
        "...",
        "...",
        "..#",
    ]
    result = parse_universe(universe)
    assert result == [
        P(0, 0),
        P(5, 3),
    ]


def test_left_boundary():
    universe = [
        "..",
        ".#",
    ]
    result = parse_universe(universe)
    assert result == [P(2, 2)]


def test_l1():
    assert l1(P(0, 0), P(0, 0)) == 0
    assert l1(P(0, 0), P(0, 1)) == 1
    assert l1(P(0, 0), P(1, 0)) == 1
    assert l1(P(0, 0), P(1, 1)) == 2


def test_p1():
    universe = [
        "...#......",
        ".......#..",
        "#.........",
        "..........",
        "......#...",
        ".#........",
        ".........#",
        "..........",
        ".......#..",
        "#...#.....",
    ]
    galaxys = parse_universe(universe)
    assert P(6, 1) in galaxys
    assert calculate_distance(galaxys) == 374


def test_p2():
    universe = [
        "...#......",
        ".......#..",
        "#.........",
        "..........",
        "......#...",
        ".#........",
        ".........#",
        "..........",
        ".......#..",
        "#...#.....",
    ]
    galaxys = parse_universe(universe, 100)
    assert calculate_distance(galaxys) == 8410
