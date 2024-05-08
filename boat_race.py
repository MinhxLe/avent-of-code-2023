import math


def calculate_travel_distance(race_ms: int, wait_ms: int) -> int:
    assert wait_ms <= race_ms
    run_ms = race_ms - wait_ms
    return run_ms * wait_ms


def get_num_ways(race_ms: int, min_distance: int) -> int:
    num_ways = 0
    for wait_ms in range(race_ms + 1):
        if calculate_travel_distance(race_ms, wait_ms) >= min_distance:
            num_ways += 1
    return num_ways


def get_num_ways_fast(race_ms: int, min_distance: int) -> int:
    """
    (R-W)*W >= T
    RW -W^2 >= T
    W^2 - RW +T <= 0

    -b +- math.sq

    """
    coef = math.sqrt(race_ms**2 - 4 * min_distance) / 2
    min_wait_ms = min(race_ms - math.floor(coef), race_ms)
    max_wait_ms = max(race_ms + math.floor(coef), race_ms)
    return max_wait_ms - min_wait_ms


times = [40929790]
distances = [215106415051100]
num_ways = []

for time, distance in zip(times, distances):
    num_ways.append(get_num_ways_fast(time, distance))
