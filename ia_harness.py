"""
Harness the IA bots and display stats about their performance.
"""
from collections import Counter
# import time
from multiprocessing import Pool

from game import Game

THREAD_COUNT = 4


class Harness(object):

    def __init__(self, ia1_class, ia2_class):
        self.game = Game()
        self.ia1_class = ia1_class
        self.ia2_class = ia2_class

    def one_game(self, proc_id=None):
        """ Run one game against the two bots """
        self.game.init_game()

        # Init the bots
        self.ia1 = self.ia1_class(self.game, 'A')
        self.ia2 = self.ia2_class(self.game, 'B')

        # start = time.time()
        step = 1
        while not self.game.victory_reached():
            player_ia = self.ia1 if step % 2 == 0 else self.ia2
            zone_played = player_ia.choose_absolute_move()
            self.game.play(zone_id=zone_played, player=player_ia.player_name)
            # print(f"\tStep {step}, player {player_ia.player_name} ({player_ia.strategy}) played {zone_played}")
            step += 1
        winner = self.game.victory_reached()
        # duration = round((time.time() - start) * 1000)
        # print(f"Game finished, player {winner} won in {step} step / {duration}ms")
        return winner

    def average(self, N=100):
        """ Run N games between the bots and show the performance """
        print(f"Running {N} iterations of A ({self.ia1_class.strategy}) against B ({self.ia2_class.strategy})")
        with Pool(THREAD_COUNT) as pool:
            stats = Counter(pool.map(self.one_game, range(N)))
        print(f"{N} iterations complete, scores={stats}")
        winner, count = stats.most_common()[0]
        win_ratio = round(count / N * 100, 1)
        perf = round((2 * count - N) / (N - count) * 100)
        strategy = (self.ia1_class if winner == 'A' else self.ia2_class).strategy
        print(f"Agent {winner} (strategy={strategy}) won in {win_ratio}% of the tests, performance is {perf}% better.")
        return stats


if __name__ == '__main__':
    import bots

    harness = Harness(bots.RandomIA, bots.MostRightBot)
    harness.average(20000)
