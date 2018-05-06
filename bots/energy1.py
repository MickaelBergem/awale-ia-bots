import logging
import random

from game import Game

from .base_bot import BaseBot


class Energy1Bot(BaseBot):
    """
    IA Random bot. A bot always assume she is playing as Player A.

    The board is ordered this way:
         0  1  2  3  4  5
        11 10  9  8  7  6
    The following zones belong to the given users:
        A A A A A A
        B B B B B B
    """

    strategy = 'energy-minimizer'

    def choose_move(self):
        """ Return the zone_id to play """
        self.board = self.relative_board()
        self.possible_zones = list(id for id, zone in enumerate(self.board[0:6]) if zone > 0)
        logging.debug(f"Player {self.player_name}: possible_zones are {self.possible_zones}")
        self.scenarios = {}
        # For each zone, check if one is winning
        next_winning_zone = self.win_next_move()
        if next_winning_zone is not None:
            return next_winning_zone
        # Compute the energy for each scenario
        best_move = None
        best_value = None
        scenarios_energy = {}
        for zone in self.possible_zones:
            scenarios_energy[zone] = self.energy(self.scenarios[zone].zones)
            if not best_value or best_value >= scenarios_energy[zone]:
                best_move = zone
                best_value = scenarios_energy[zone]

        if best_move is not None:
            return best_move

        # No winning zone, fall back to random
        return random.choice(self.possible_zones)

    def win_next_move(self):
        """ Return the move that wins the game or None """
        for zone in self.possible_zones:
            self.scenarios[zone] = Game(self.board)
            self.scenarios[zone].play(zone)
            if self.scenarios[zone].victory_reached():
                return zone
        return None

    @staticmethod
    def energy(board):
        """ Return the energy value for the given board """
        return sum(board[0:6])
