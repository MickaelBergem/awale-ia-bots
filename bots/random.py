import logging
import random

from .base_bot import BaseBot


class RandomIA(BaseBot):
    """
    IA Random bot. A bot always assume she is playing as Player A.

    The board is ordered this way:
         0  1  2  3  4  5
        11 10  9  8  7  6
    The following zones belong to the given users:
        A A A A A A
        B B B B B B
    """

    strategy = 'random'

    def choose_move(self):
        """ Return the zone_id to play """
        board = self.relative_board()[0:6]
        possible_zones = list(id for id, zone in enumerate(board) if zone > 0)
        logging.debug(f"Player {self.player_name}: possible_zones are {possible_zones}")
        return random.choice(possible_zones)
