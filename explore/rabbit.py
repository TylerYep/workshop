from __future__ import annotations

import random


class RabbitFinder3000:
    def __init__(self, num_holes: int) -> None:
        self.num_holes = num_holes
        self.prev_guesses = []

    def guess(self) -> int:
        guess = -1
        # first guess
        if not self.prev_guesses or self.num_holes == 2:
            guess = 1
        else:
            # staircase down
            if max(self.prev_guesses) == self.num_holes - 2:
                guess = self.prev_guesses[-1] - 1

            else:
                num_of_prev = 0
                for i in self.prev_guesses[::-1]:
                    if i == self.prev_guesses[-1]:
                        num_of_prev += 1

                if num_of_prev == 2:
                    guess = self.prev_guesses[-1] + 1
                else:
                    guess = self.prev_guesses[-1]

        self.prev_guesses.append(guess)
        return guess


def play_game(num_holes: int, use_algorithm: bool) -> bool:
    holes = [False for _ in range(num_holes)]
    rabbit = random.randrange(num_holes)
    holes[rabbit] = True

    solver = RabbitFinder3000(num_holes=num_holes)
    count = 0
    # print(holes)
    while True:
        if use_algorithm:
            choice_index = solver.guess()
            if count > num_holes ** 2:
                print(solver.prev_guesses)
                print(f"You lost after {count} guesses!!")
                return count
        else:
            guess = input(f"What index is the rabbit (0-{num_holes - 1})? ")
            if not guess:
                print(f"You lost after {count} guesses!!")
                return count
            choice_index = int(guess)

        count += 1
        if holes[choice_index]:
            if use_algorithm:
                print(solver.prev_guesses)
            print(f"You won in {count} guesses!!")
            return count

        holes[rabbit] = False
        if rabbit == 0:
            rabbit += 1
        elif rabbit == num_holes - 1:
            rabbit -= 1
        else:
            rabbit += random.choice([-1, 1])
        holes[rabbit] = True


if __name__ == "__main__":
    play_game(4, False)
