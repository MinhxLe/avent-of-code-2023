from fertilizer_v2 import Range, RangeMap, map_range, RangeMapSet


def test_range_intersect():
    assert Range(0, 10).intersect(Range(5, 15)) == Range(5, 10)
    assert Range(5, 15).intersect(Range(0, 10)) == Range(5, 10)
    assert Range(0, 10).intersect(Range(10, 15)) is None


def test_range_minus():
    assert Range(0, 10).diff(Range(10, 15)) == {Range(0, 10)}
    assert Range(0, 10).diff(Range(-5, 0)) == {Range(0, 10)}

    assert Range(0, 10).diff(Range(-1, 5)) == {Range(5, 10)}
    assert Range(0, 10).diff(Range(5, 10)) == {Range(0, 5)}
    assert Range(0, 10).diff(Range(3, 7)) == {Range(0, 3), Range(7, 10)}


def test_range_map():
    m = RangeMap(Range(0, 10), 5)
    assert m.map(Range(0, 3)) == (Range(5, 8), set())
    assert m.map(Range(0, 13)) == (Range(5, 15), {Range(10, 13)})
    assert m.map(Range(-1, 13)) == (Range(5, 15), {Range(-1, 0), Range(10, 13)})
    assert m.map(Range(10, 15)) == (None, {Range(10, 15)})


def test_map_range():
    range = Range(0, 10)
    map_set = RangeMapSet(
        "a",
        "b",
        set(
            [
                RangeMap(Range(0, 3), 1),
                RangeMap(Range(3, 6), 2),
            ]
        ),
    )
    assert map_range(range, "a", "b", [map_set]) == {
        Range(1, 4),
        Range(5, 8),
        Range(6, 10),  # we probably should merge
    }


def test_map_range_chain():
    range = Range(0, 10)
    map_set1 = RangeMapSet(
        "a",
        "b",
        set(
            [
                RangeMap(Range(0, 10), 1),
            ]
        ),
    )
    map_set2 = RangeMapSet(
        "b",
        "c",
        set(
            [
                RangeMap(Range(1, 11), 1),
            ]
        ),
    )
    assert map_range(range, "a", "c", [map_set1, map_set2]) == {
        Range(2, 12),
    }
