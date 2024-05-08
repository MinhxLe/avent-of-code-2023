from dataclasses import dataclass
import functools
from typing import List
import utils


@dataclass
class Draw:
    red: int = 0
    green: int = 0
    blue: int = 0

    def power(self) -> int:
        return self.red * self.green * self.blue


def merge_draws(d1: Draw, d2: Draw) -> Draw:
    return Draw(
        max(d1.red, d2.red),
        max(d1.green, d2.green),
        max(d1.blue, d2.blue),
    )


@dataclass
class Game:
    id: int
    draws: List[Draw]


def is_draw_possible(draw: Draw) -> bool:
    return draw.red <= 12 and draw.green <= 13 and draw.blue <= 14


def is_game_possible(game: Game) -> bool:
    return all([is_draw_possible(draw) for draw in game.draws])


def parse_draw(text: str) -> Draw:
    draw = Draw(0, 0, 0)
    for color_text in text.split(", "):
        count, color = color_text.split(" ")
        count = int(count)
        if color == "red":
            draw.red += count
        elif color == "green":
            draw.green += count
        elif color == "blue":
            draw.blue += count
        else:
            raise ValueError
    return draw


def parse_game(line: str) -> Game:
    [game_text, draw_text] = line.split(": ")
    return Game(
        id=int(game_text[len("Game ") :]),
        draws=[parse_draw(d) for d in draw_text.split("; ")],
    )


lines = utils.read_lines("cubes.txt")
games = [parse_game(g) for g in lines]

print("Question 2")
possible_games = [g for g in games if is_game_possible(g)]
print(sum([g.id for g in possible_games]))

print("Question 3")
total_sum = 0
for game in games:
    final_draw = functools.reduce(merge_draws, game.draws, Draw())
    total_sum += final_draw.power()
print(total_sum)
