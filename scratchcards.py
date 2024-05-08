import re
import utils
from dataclasses import dataclass
from collections import Counter


@dataclass
class Card:
    id: int
    target_nums: set[int]
    candidate_nums: set[int]


def _assert_unique(x: list):
    assert len(set(x)) == len(x)


def lm(fn, iterable):
    return list(map(fn, iterable))


def _extract_nums(s: str) -> list[int]:
    nums = re.findall(r"\d+", s)
    return lm(int, nums)


def parse_card(raw_card: str) -> Card:
    pattern = r"^Card\s+(\d+): (.*)$"
    match = re.search(pattern, raw_card)
    id, numbers = match.groups((1, 2))
    raw_target_nums, raw_candidate_nums = numbers.split("|")
    target_nums = _extract_nums(raw_target_nums)
    candidate_nums = _extract_nums(raw_candidate_nums)

    _assert_unique(target_nums)
    _assert_unique(candidate_nums)

    return Card(int(id), set(target_nums), set(candidate_nums))


def get_matching_count(card: Card) -> int:
    return len(card.target_nums - (card.target_nums - card.candidate_nums))


def calculate_card_point(card: Card) -> int:
    matching_count = get_matching_count(card)
    if matching_count >= 1:
        return 2 ** (matching_count - 1)
    else:
        return 0


def get_total_card_count(cards: list[Card]) -> int:
    card_counts = Counter()
    for card in cards:
        card_counts[card.id] += 1
        card_points = get_matching_count(card)
        for copy_id in range(card.id + 1, card.id + 1 + card_points):
            card_counts[copy_id] += card_counts[card.id]
    return sum(card_counts.values())


lines = utils.read_lines("scratchcards.txt")
cards = lm(parse_card, lines)
points = lm(calculate_card_point, cards)
print(sum(points))
print(get_total_card_count(cards))
