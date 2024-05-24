from fertilizer import MapRangeEncoding, get_map_fn, Map, map_paths


def test_get_map_fn():
    fn = get_map_fn([MapRangeEncoding(5, 10, 10)])
    assert fn(8) == 13
    assert fn(4) == 4
    assert fn(16) == 16

    fn = get_map_fn([MapRangeEncoding(10, 5, 10)])
    assert fn(8) == 8
    assert fn(16) == 11


def test_map_paths():
    assert map_paths(1, "a", "b", [Map("a", "b", lambda x: x + 1)]) == 2


def test_map_paths_multiple():
    assert (
        map_paths(
            1,
            "a",
            "c",
            [
                Map("a", "b", lambda x: x + 1),
                Map("b", "c", lambda x: x + 2),
            ],
        )
        == 4
    )
