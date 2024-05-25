from dataclasses import dataclass
import re
from typing import Optional, Tuple


@dataclass(frozen=True)
class Range:
    start: int
    end: int

    def __post__init__(self):
        assert self.start < self.end

    def intersect(self, that: "Range") -> Optional["Range"]:
        new_start = max(self.start, that.start)
        new_end = min(self.end, that.end)

        if new_start < new_end:
            return Range(new_start, new_end)
        else:
            return None

    def diff(self, that: "Range") -> set["Range"]:
        ranges = set()

        if that.end <= self.start:
            ranges.add(self)
        elif self.end <= that.start:
            ranges.add(self)
        else:
            if self.start < that.start:
                ranges.add(Range(self.start, that.start))
            if that.end < self.end:
                ranges.add(Range(that.end, self.end))
        return ranges

    def shift(self, offset: int) -> "Range":
        return Range(self.start + offset, self.end + offset)


@dataclass(frozen=True)
class RangeMap:
    range: Range
    offset: int

    def map(self, range: Range) -> Tuple[Optional[Range], set[Range]]:
        range_to_map = range.intersect(self.range)
        if range_to_map is not None:
            mapped_range = range_to_map.shift(self.offset)
            unmapped_range = range.diff(range_to_map)
        else:
            mapped_range = None
            unmapped_range = {range}

        return (mapped_range, unmapped_range)


@dataclass
class RangeMapSet:
    source_type: str
    dest_type: str
    maps: set[RangeMap]

    def map(self, range: Range) -> set[Range]:
        all_mapped_ranges = set()
        all_unmapped_ranges = {range}
        for map in self.maps:
            all_new_unmapped_ranges = set()
            while all_unmapped_ranges:
                curr_range = all_unmapped_ranges.pop()
                new_mapped_range, new_unmapped_ranges = map.map(curr_range)
                if new_mapped_range:
                    all_mapped_ranges.add(new_mapped_range)
                all_new_unmapped_ranges |= new_unmapped_ranges
            all_unmapped_ranges = all_new_unmapped_ranges
        return all_mapped_ranges | all_unmapped_ranges


def map_range(
    range: Range,
    source_type: str,
    dest_type: str,
    map_sets: list[RangeMapSet],
) -> set[Range]:
    curr_source_type = source_type
    curr_ranges = {range}

    while curr_source_type != dest_type:
        for map_set in map_sets:
            if map_set.source_type == curr_source_type:
                new_ranges = set()
                for range in curr_ranges:
                    new_ranges |= map_set.map(range)
                curr_ranges = new_ranges
                curr_source_type = map_set.dest_type
                break
    return curr_ranges


seeds = None
map_sets = []
with open("./fertilizer.txt") as file:
    source_type, dest_type, maps = None, None, []
    for line in file:
        line = line.rstrip()
        # seed line
        if (match := re.match(r"^seeds: (.*)$", line)) is not None:
            numbers = [int(i) for i in match.group(1).split(" ")]
            seeds = [
                Range(numbers[i], numbers[i] + numbers[i + 1])
                for i in range(0, len(numbers) - 1, 2)
            ]
        # map spec line
        elif (match := re.match(r"^(\w+)-to-(\w+) map:$", line)) is not None:
            source_type, dest_type = match.groups((1, 2))
        # number line
        elif (match := re.match(r"^(\d+) (\d+) (\d+)$", line)) is not None:
            dest_start, source_start, length = match.groups((1, 2, 3))
            maps.append(
                RangeMap(
                    Range(int(source_start), int(source_start) + int(length)),
                    int(dest_start) - int(source_start),
                )
            )
        else:
            if source_type:
                map_sets.append(RangeMapSet(source_type, dest_type, set(maps)))
            source_type, dest_type, maps = None, None, []
    if source_type:
        map_sets.append(RangeMapSet(source_type, dest_type, set(maps)))

location_ranges = set()
for seed in seeds:
    location_ranges |= map_range(seed, "seed", "location", map_sets)
