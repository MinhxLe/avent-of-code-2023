from typing import Tuple


def find_extrapolation(nums: list[int]) -> int:
    if len(nums) == 0:
        return 0
    if all([d == 0 for d in nums]):
        return 0
    diffs = [nums[i + 1] - nums[i] for i in range(len(nums) - 1)]
    return find_extrapolation(diffs) + nums[-1]


def find_extrapolation_backwards(nums: list[int]) -> int:
    if len(nums) == 0:
        return 0
    if all([d == 0 for d in nums]):
        return 0
    diffs = [nums[i + 1] - nums[i] for i in range(len(nums) - 1)]
    x = find_extrapolation_backwards(diffs)
    print(f"{x}, {nums[0]-x} {nums}")
    return nums[0] - x


seq = [int(i) for i in "10 13 16 21 30 45".split(" ")]
print(find_extrapolation_backwards(seq))


with open("./mirage_9.txt") as f:
    lines = [l for l in f]

seqs = [[int(i) for i in l.split(" ")] for l in lines]
extrapolations = map(find_extrapolation, seqs)
extrapolations_backwards = map(find_extrapolation_backwards, seqs)
