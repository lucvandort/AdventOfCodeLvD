from tqdm import tqdm
from collections import deque, defaultdict

# %% Marblegable class definition


class Marblegame():

    def __init__(self, num_players, num_marbles):
        self.num_players = num_players
        self.num_marbles = num_marbles

        self.players = list(range(1, self.num_players+1))
        self.reset_game()

    def __str__(self):
        return (
            f"Marblegame with {self.num_players} players and "
            f"{self.num_marbles} marbles."
        )

    def reset_game(self):
        self.marbles = list(range(0, self.num_marbles))
        self.gamecircle = deque()
        self.scoreboard = defaultdict(int)
        self.current_player = self.players[-1]
        self.current_marble = 0
        self.gamecircle.append(self.marbles[self.current_marble])
        self.gamelength = 1

    def place_marble(self):
        try:
            next_marble = self.marbles[self.current_marble + 1]
        except IndexError:
            return -1

        self.current_player = self.players[
            (self.players.index(self.current_player) + 1)
            % self.num_players
        ]

        if next_marble % 23 == 0 and next_marble > 0:
            self.scoreboard[self.current_player] += next_marble
            self.gamecircle.rotate(7)
            self.scoreboard[self.current_player] += \
                self.gamecircle.pop()
            self.gamecircle.rotate(-1)
        else:
            self.gamecircle.rotate(-1)
            self.gamecircle.append(next_marble)

        self.gamelength += 1
        self.current_marble = next_marble
        return self.current_marble

    def play_game(self):
        with tqdm(total=self.num_marbles) as pbar:
            while self.gamelength < self.num_marbles:
                self.place_marble()
                pbar.update()

    def highest_score(self):
        return max(self.scoreboard.values())


# %% testgames
print("\n=== example ===")
testgame = Marblegame(num_players=9, num_marbles=25+1)
print(testgame)
while testgame.place_marble() >= 0:
    print(testgame.current_player, testgame.gamecircle)
print(testgame.scoreboard)
print(testgame.highest_score())
assert testgame.highest_score() == 32


# %% more testgames

print("\n=== testgame 2 ===")
testgame2 = Marblegame(num_players=10, num_marbles=1618+1)
print(testgame2)
testgame2.play_game()
print(testgame2.scoreboard)
print(testgame2.highest_score())
assert testgame2.highest_score() == 8317

print("\n=== testgame 3 ===")
testgame3 = Marblegame(num_players=13, num_marbles=7999+1)
print(testgame3)
testgame3.play_game()
print(testgame3.scoreboard)
print(testgame3.highest_score())
assert testgame3.highest_score() == 146373

print("\n=== testgame 4 ===")
testgame4 = Marblegame(num_players=17, num_marbles=1104+1)
print(testgame4)
testgame4.play_game()
print(testgame4.scoreboard)
print(testgame4.highest_score())
assert testgame4.highest_score() == 2764

print("\n=== testgame 5 ===")
testgame5 = Marblegame(num_players=21, num_marbles=6111+1)
print(testgame5)
testgame5.play_game()
print(testgame5.scoreboard)
print(testgame5.highest_score())
assert testgame5.highest_score() == 54718

print("\n=== testgame 6 ===")
testgame6 = Marblegame(num_players=30, num_marbles=5807+1)
print(testgame6)
testgame6.play_game()
print(testgame6.scoreboard)
print(testgame6.highest_score())
assert testgame6.highest_score() == 37305


# %% Part 1

print("\n=== Part 1 ===")

with open('input.txt') as inputfile:
    line = inputfile.read().split()

num_players = int(line[0])
last_marble_worth = int(line[6])

part1_game = Marblegame(
    num_players=num_players,
    num_marbles=last_marble_worth+1,
)
print(part1_game)
part1_game.play_game()
# print(part1_game.scoreboard)
print(f"The winning Elf's score is {part1_game.highest_score()}.")

# %% Part 2
print("\n=== Part 2 ===")

part2_game = Marblegame(
    num_players=num_players,
    num_marbles=(last_marble_worth*100)+1,
)
print(part2_game)
part2_game.play_game()
# print(part2_game.scoreboard)
print(f"The winning Elf's score is {part2_game.highest_score()}.")
