from collections import defaultdict
from enum import IntEnum
from dataclasses import dataclass
from functools import cached_property
from typing import Counter
import numpy as np


@dataclass(frozen=True)
class Card:
    value: str

    VALUE_ORDERING = ["J", "2", "3", "4", "5", "6", "7", "8", "9", "T", "Q", "K", "A"]

    def __post_init__(self):
        assert self.value in self.VALUE_ORDERING

    def __lt__(self, that: "Card") -> bool:
        return self.VALUE_ORDERING.index(self.value) < self.VALUE_ORDERING.index(
            that.value
        )


class HandType(IntEnum):
    SINGLE = 1
    PAIR = 2
    TWO_PAIR = 3
    TRIPLE = 4
    FULL_HOUSE = 5
    QUAD = 6
    FIVE = 7


@dataclass
class Hand:
    cards: list[Card]
    bid: int

    def __post_init__(self):
        assert len(self.cards) == 5

    @cached_property
    def hand_type(self) -> HandType:
        wild_card = Card("J")
        counter = Counter(self.cards)
        if wild_card in counter:
            num_wild_cards = counter.pop(wild_card)
        else:
            num_wild_cards = 0
        count_to_cards = defaultdict(list)
        
        for card, count in counter.items():
            count_to_cards[count].append(card)

        if count_to_cards:
            ...
            max_count = max([count for count in count_to_cards])
            max_count_cards = count_to_cards.pop(max_count)
            count_to_cards[max_count] = max_count_cards[1:] 
            count_to_cards[max_count + num_wild_cards].append(max_count_cards[0])
        else:
            count_to_cards[5].append(wild_card)

        if len(count_to_cards[5]) == 1:
            return HandType.FIVE
        elif len(count_to_cards[4]) == 1:
            return HandType.QUAD
        elif len(count_to_cards[3]) == 1:
            if len(count_to_cards[2]) == 1:
                return HandType.FULL_HOUSE
            else:
                return HandType.TRIPLE
        elif len(count_to_cards[2]) > 0:
            if len(count_to_cards[2]) == 2:
                return HandType.TWO_PAIR
            else:
                return HandType.PAIR
        else:
            return HandType.SINGLE

    def __lt__(self, that: "Hand") -> bool:
        return (self.hand_type, *self.cards) < (that.hand_type, *that.cards)
        if self.hand_type != self.hand_type:
            return self.hand_type < self.hand_type
        else:
            for card1, card2 in zip(self.cards, that.cards):
                if card1 != card2:
                    return card1 < card2
        raise NotImplementedError

    def __repr__(self) -> str:
        return "".join([c.value for c in self.cards]) + f" {self.hand_type.name}"


hands = []
with open("./camel_card.txt") as f:
    for line in f:
        raw_hand, raw_bid = line.split(" ")
        hands.append(Hand([Card(c) for c in raw_hand], int(raw_bid)))
hands.sort()
total = 0
for i, hand in enumerate(hands):
    print(f"{hand} {hand.bid} {i}")
    total += (i+1)*hand.bid
print(total)
