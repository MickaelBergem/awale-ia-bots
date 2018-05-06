import logging
import random

from game import Game

from .base_bot import BaseBot


class Naive1Bot(BaseBot):
    """
    IA Random bot. A bot always assume she is playing as Player A.

    The board is ordered this way:
         0  1  2  3  4  5
        11 10  9  8  7  6
    The following zones belong to the given users:
        A A A A A A
        B B B B B B
    """

    strategy = 'last-step-victory'

    def choose_move(self):
        """ Return the zone_id to play """
        board = self.relative_board()
        possible_zones = list(id for id, zone in enumerate(board[0:6]) if zone > 0)
        logging.debug(f"Player {self.player_name}: possible_zones are {possible_zones}")
        # For each zone, check if one is winning
        for zone in possible_zones:
            scenario = Game(board)
            scenario.play(zone)
            if scenario.victory_reached():
                return zone
        # No winning zone, fall back to random
        return random.choice(possible_zones)
