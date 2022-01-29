from __future__ import annotations

import itertools
import random


class RabbitGameState:
    def __init__(self, num_holes: int, verbose: bool) -> None:
        self.holes = [False for _ in range(num_holes)]
        self.rabbit = random.randrange(num_holes)
        self.holes[self.rabbit] = True
        self.guess_count = 0
        self.verbose = verbose
        self.game_over = False
        self.num_holes = num_holes

    def add_guess(self, guess: int | None) -> None:
        if guess is None:
            self.end_game(f"You lost after {self.guess_count} guesses!!")
            return

        self.guess_count += 1
        if self.holes[guess]:
            self.end_game(f"You found the rabbit in {self.guess_count} guesses!!")
        elif self.guess_count > self.num_holes**2:
            self.end_game(f"You lost after {self.guess_count} guesses!!")
        else:
            self.rabbit_hop()

    def end_game(self, message: str) -> None:
        self.game_over = True
        if self.verbose:
            print(message)

    def rabbit_hop(self) -> None:
        self.holes[self.rabbit] = False
        if self.rabbit == 0:
            self.rabbit += 1
        elif self.rabbit == self.num_holes - 1:
            self.rabbit -= 1
        else:
            self.rabbit += random.choice([-1, 1])
        self.holes[self.rabbit] = True


class RabbitFinder3000:
    def __init__(self, num_holes: int) -> None:
        if num_holes == 1:
            self.guesses = iter([0])
        elif 2 <= num_holes <= 3:
            self.guesses = iter([1, 1])
        elif num_holes == 4:
            self.guesses = iter([1, 1, 2, 2, 1])
        else:
            self.guesses = itertools.chain(
                list(range(num_holes)),
                [1] if num_holes % 2 == 0 else [],
                list(range(num_holes)),
            )
        self.num_holes = num_holes

    def guess(self) -> int:
        return next(self.guesses)


def play_game(
    num_holes: int, use_algorithm: bool = False, verbose: bool = False
) -> int:
    rabbit_game = RabbitGameState(num_holes, verbose)
    solver = RabbitFinder3000(num_holes)
    choice_index: int | None
    while not rabbit_game.game_over:
        if use_algorithm:
            choice_index = solver.guess()
        else:
            guess = input(f"What index is the rabbit (0-{num_holes - 1})? ")
            choice_index = int(guess) if guess else None

        rabbit_game.add_guess(choice_index)

    return rabbit_game.guess_count


if __name__ == "__main__":
    play_game(4)
