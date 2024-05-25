from dataclasses import dataclass
from typing import Callable
import re


@dataclass
class Map:
    source_type: str
    dest_type: str
    map: Callable[[int], int]


@dataclass
class Range:
    start_idx: int
    length: int

    def intersect(self, that: "Range") -> Optional["Range"]:
        self_end_idx = self.start_idx + self.length
        that_end_idx = that.start_idx + that.length

        new_start_idx = max(self.start_idx, that.start_idx)
        new_end_idx = min(self_end_idx, that_end_idx)
        return Range(new_start_idx, min(0, new_end_idx - new_start_idx))

    def minus(self, that: "Range") -> set["Range"]:
        pass

    def empty(self) -> bool:
        return self.length == 0


@dataclass
class RangeMap:
    source_start_idx: int
    dest_start_idx: int
    length: int

    @classmethod
    def decode(cls, encoding: str) -> "RangeMap":
        dest_start_idx, source_start_idx, length = encoding.split(" ")
        return RangeMap(
            int(source_start_idx),
            int(dest_start_idx),
            int(length),
        )


@dataclass
class RangeMapSet:
    source_type: str
    dest_type: str
    maps: set[RangeMap]


def map_range(source_range: Range, range_map: RangeMap) -> Tuple[Range, Range]:
    start_idx, length2
    start_idx, length2

    pass


def map_range_paths(
    source_ranges: Range,
    source_type: str,
    dest_type: str,
    map_sets: list[RangeMapSet],
) -> set[Range]:
    pass


def get_map_fn(mappings: list[RangeMap]) -> Callable[[int], int]:
    def _map(source_idx: int) -> int:
        for encoding in mappings:
            offset = source_idx - encoding.source_start_idx
            if 0 <= offset and offset <= encoding.length:
                return encoding.dest_start_idx + offset
        return source_idx

    return _map


def map_paths(
    start_idx: int,
    source_type: str,
    dest_type: str,
    maps: list[Map],
) -> int:
    curr_source_type = source_type
    curr_start_idx = start_idx
    while curr_source_type != dest_type:
        for map in maps:
            if map.source_type == curr_source_type:
                curr_start_idx = map.map(curr_start_idx)
                curr_source_type = map.dest_type
                break
    return curr_start_idx


seeds = None
maps = []
with open("./fertilizer.txt") as file:
    source_type, dest_type, mappings = None, None, []
    for line in file:
        line = line.rstrip()
        # seed line
        if (match := re.match(r"^seeds: (.*)$", line)) is not None:
            seeds = [int(i) for i in match.group(1).split(" ")]
        # map spec line
        elif (match := re.match(r"^(\w+)-to-(\w+) map:$", line)) is not None:
            source_type, dest_type = match.groups((1, 2))
        # number line
        elif (match := re.match(r"^(\d+) (\d+) (\d+)$", line)) is not None:
            dest_idx, source_idx, length = match.groups((1, 2, 3))
            mappings.append(RangeMap(int(source_idx), int(dest_idx), int(length)))
        else:
            if source_type:
                maps.append(Map(source_type, dest_type, get_map_fn(mappings)))
            source_type, dest_type, mappings = None, None, []
    if source_type:
        maps.append(Map(source_type, dest_type, get_map_fn(mappings)))


locations = []
for seed in seeds:
    locations.append(map_paths(seed, "seed", "location", maps))
print(min(locations))
