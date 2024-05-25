import pytest
from reflection_13 import (
    is_horizonal_reflection,
    is_vertical_reflection,
    summarize_image,
    summarize_images,
    transpose,
)


def parse_images(lines: list[str]):
    images = []
    image = []
    for line in lines:
        if line == "":
            images.append(image)
            image = []
        else:
            image.append(line)
    return images


def test_is_vertical_reflection():
    assert is_vertical_reflection(["##"], 0) is True
    assert is_vertical_reflection(["#."], 0) is False
    # multiple
    assert is_vertical_reflection(["#..#"], 1) is True
    # out of boundary
    assert is_vertical_reflection(["#..."], 2) is True
    # multiple rows
    assert (
        is_vertical_reflection(
            ["#..#" ".##."],
            1,
        )
        is True
    )


def test_is_horizonal_reflection():
    assert is_horizonal_reflection(["#", "#"], 0) is True
    assert is_horizonal_reflection(["#", "."], 0) is False
    # multiple
    assert is_horizonal_reflection(["#", ".", ".", "#"], 1) is True
    # oob
    assert is_horizonal_reflection(["#", ".", ".", "."], 2) is True
    assert is_horizonal_reflection(["##", "##"], 0) is True


def test_is_horizonal_reflection_smudge_count():
    assert is_horizonal_reflection(["#", "."], 0) is False
    assert is_horizonal_reflection(["#", "."], 0, 1) is True

    assert is_horizonal_reflection(["#", "#"], 0, 1) is False
    # 2 smudge
    assert is_horizonal_reflection([".", ".", "#", "#"], 1, 1) is False

    assert is_horizonal_reflection(["..", "##"], 1, 1) is False
    assert is_horizonal_reflection(["..", "..", "..", "##"], 1, 1) is False


def test_transpose():
    assert transpose(["1"]) == ["1"]
    assert transpose(["12"]) == ["1", "2"]
    assert transpose(["1", "2"]) == ["12"]


def test_summarize_image():
    images = [
        [
            "#.##..##.",
            "..#.##.#.",
            "##......#",
            "##......#",
            "..#.##.#.",
            "..##..##.",
            "#.#.##.#.",
        ],
        [
            "#...##..#",
            "#....#..#",
            "..##..###",
            "#####.##.",
            "#####.##.",
            "..##..###",
            "#....#..#",
        ],
    ]
    assert summarize_images(images) == 405


def test_summarize_image_p2():
    raw_images = """#.##..##.
..#.##.#.
##......#
##......#
..#.##.#.
..##..##.
#.#.##.#.

#...##..#
#....#..#
..##..###
#####.##.
#####.##.
..##..###
#....#..#

.#.##.#.#
.##..##..
.#.##.#..
#......##
#......##
.#.##.#..
.##..##.#

#..#....#
###..##..
.##.#####
.##.#####
###..##..
#..#....#
#..##...#

#.##..##.
..#.##.#.
##..#...#
##...#..#
..#.##.#.
..##..##.
#.#.##.#."""
    images = parse_images(raw_images.split("\n"))
    assert summarize_images(images)


@pytest.mark.skip
def test_asdf():
    image = [
        ".##..##",
        "###..##",
        "#..##..",
        "#..##..",
        "##....#",
        ".##..##",
        "##.##.#",
        "###..##",
        ".##..##",
        "..#..#.",
        ".#.##.#",
    ]
    assert is_horizonal_reflection(image, 2, 1) is False
