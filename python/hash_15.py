from dataclasses import dataclass
from typing import Optional
import re


def hash_string(s: str) -> int:
    val = 0
    for c in s:
        val += ord(c)
        val *= 17
        val %= 256
    return val


def find_idx(l: list, filter_fn) -> int | None:
    for i, e in enumerate(l):
        if filter_fn(e):
            return i
    else:
        return None


@dataclass
class Lens:
    label: str
    power: int


@dataclass
class Box:
    label: int
    lenses: list[Lens]

    def create_or_update(self, label: str, power: int):
        idx = find_idx(self.lenses, lambda x: x.label == label)
        if idx is not None:
            self.lenses[idx].power = power
        else:
            self.lenses.append(Lens(label, power))
        if not len(set(map(lambda x: x.label, self.lenses))) == len(self.lenses):
            __import__("ipdb").set_trace()

    def remove(self, label: str) -> Optional[Lens]:
        idx = find_idx(self.lenses, lambda x: x.label == label)
        if idx is not None:
            return self.lenses.pop(idx)
        else:
            return None

    def power(self) -> int:
        total = 0
        for i, lens in enumerate(self.lenses):
            total += (1 + self.label) * (i + 1) * lens.power
        return total


def compute_power(box: Box) -> int:
    total = 0
    for i, lens in enumerate(box.lenses):
        total += (1 + box.label) * (i + 1) * lens.power
    return total


def get_boxes(commands: list[str]) -> list[Box]:
    boxes = [Box(i, []) for i in range(256)]
    for command in commands:
        if (match := re.match(r"^(.*)=([1-9])$", command)) is not None:
            label, power = match.groups((1, 2))
            boxes[hash_string(label)].create_or_update(label, int(power))
        elif match := re.match(r"^(.*)-$", command):
            (label,) = match.groups((1,))
            boxes[hash_string(label)].remove(label)
            pass
        else:
            print(command)
    return boxes


with open("./hash_15.txt") as f:
    line = f.readline().strip()

words = line.split(",")

# part 1
print(sum([hash_string(w) for w in words]))

# part2
# boxes = get_boxes("rn=1,cm-,qp=3,cm=2,qp-,pc=4,ot=9,ab=5,pc-,pc=6,ot=7".split(","))
boxes = get_boxes(words)
print(sum([b.power() for b in boxes]))
