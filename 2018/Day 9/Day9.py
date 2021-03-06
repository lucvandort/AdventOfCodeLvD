from tqdm import tqdm
import numpy as np

# %% Marblegable class definition


class Marblegame():

    def __init__(self, num_players, num_marbles):
        self.num_players = num_players
        self.num_marbles = num_marbles

        self.players = np.arange(1, self.num_players+1, dtype=int)
        self.reset_game()

    def __str__(self):
        return (
            f"Marblegame with {self.num_players} players and "
            f"{self.num_marbles} marbles."
        )

    def reset_game(self):
        self.marbles = np.arange(1, self.num_marbles, dtype=int)
        self.gamecircle = np.zeros(self.num_marbles, dtype=int)
        self.scoreboard = {p: 0 for p in self.players}
        self.current_player = self.players[-1]
        self.current_marble = 0
        self.gamelength = 1

    def place_marble(self):
        try:
            next_marble = self.marbles[0]
            self.marbles = np.delete(self.marbles, 0)
        except IndexError:
            return -1

        self.current_player = self.players[
            (np.where(self.players == self.current_player)[0][0] + 1)
            % self.num_players
        ]

        if next_marble % 23 == 0 and next_marble > 0:
            self.scoreboard[self.current_player] += next_marble
            next_marble_index = \
                (self.current_marble - 7) % self.gamelength
            self.scoreboard[self.current_player] += \
                self.gamecircle[next_marble_index]
            self.gamecircle[next_marble_index:self.gamelength-1] = \
                self.gamecircle[next_marble_index+1:self.gamelength]
            self.gamelength -= 1
        else:
            next_marble_index = \
                (self.current_marble + 2) % self.gamelength
            if next_marble_index == 0:
                next_marble_index = self.gamelength
            self.gamecircle[next_marble_index+1:self.gamelength+1] = \
                self.gamecircle[next_marble_index:self.gamelength]
            self.gamecircle[next_marble_index] = next_marble
            self.gamelength += 1

        self.current_marble = next_marble_index
        return self.current_marble

    def play_game(self):
        with tqdm(total=self.num_marbles) as pbar:
            while len(self.marbles) > 0:
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


# %%
print("\n=== testgame 2 ===")
testgame2 = Marblegame(num_players=10, num_marbles=1618+1)
print(testgame2)
testgame2.play_game()
print(testgame2.scoreboard)
print(testgame2.highest_score())

print("\n=== testgame 3 ===")
testgame3 = Marblegame(num_players=13, num_marbles=7999+1)
print(testgame3)
testgame3.play_game()
print(testgame3.scoreboard)
print(testgame3.highest_score())

print("\n=== testgame 4 ===")
testgame4 = Marblegame(num_players=17, num_marbles=1104+1)
print(testgame4)
testgame4.play_game()
print(testgame4.scoreboard)
print(testgame4.highest_score())

print("\n=== testgame 5 ===")
testgame5 = Marblegame(num_players=21, num_marbles=6111+1)
print(testgame5)
testgame5.play_game()
print(testgame5.scoreboard)
print(testgame5.highest_score())

print("\n=== testgame 6 ===")
testgame6 = Marblegame(num_players=30, num_marbles=5807+1)
print(testgame6)
testgame6.play_game()
print(testgame6.scoreboard)
print(testgame6.highest_score())

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
#print("\n=== Part 2 ===")
#
#part2_game = Marblegame(
#    num_players=num_players,
#    num_marbles=(last_marble_worth*100)+1,
#)
#print(part2_game)
#part2_game.play_game()
## print(part2_game.scoreboard)
#print(f"The winning Elf's score is {part2_game.highest_score()}.")
