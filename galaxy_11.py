from dataclasses import dataclass


@dataclass
class P:
    x: int
    y: int


def l1(p1: P, p2: P) -> int:
    return abs(p1.x - p2.x) + abs(p1.y - p2.y)


@dataclass
class Universe:
    galaxys: list[P]


def parse_universe(universe: list[str], expansion_factor: int = 2) -> list[P]:
    n_rows = len(universe)
    n_cols = len(universe[0])
    galaxys = []
    for i in range(n_rows):
        for j in range(n_cols):
            if universe[i][j] == "#":
                galaxys.append(P(i, j))

    empty_rows = [i for i in range(n_rows) if i not in set(map(lambda p: p.x, galaxys))]
    empty_cols = [i for i in range(n_cols) if i not in set(map(lambda p: p.y, galaxys))]

    p, count = 0, 0
    galaxys.sort(key=lambda g: g.x)
    # we add an empty row at the end to handle the edge case of galaxys at the boundar
    for empty_row in empty_rows + [n_rows]:
        while p < len(galaxys) and galaxys[p].x < empty_row:
            galaxys[p].x += count
            p += 1
        count += expansion_factor - 1

    p, count = 0, 0
    galaxys.sort(key=lambda g: g.y)
    for empty_col in empty_cols + [n_cols]:
        while p < len(galaxys) and galaxys[p].y < empty_col:
            galaxys[p].y += count
            p += 1
        count += expansion_factor - 1
    return galaxys


def calculate_distance(galaxys: list[P]) -> int:
    total_distance = 0
    for i in range(len(galaxys)):
        for j in range(i + 1, len(galaxys)):
            total_distance += l1(galaxys[i], galaxys[j])
    return total_distance


with open("./galaxy_11.txt") as f:
    universe = [l.rstrip() for l in f]
galaxys = parse_universe(universe, 1_000_000)
print(calculate_distance(galaxys))
