"""
Game Engine API
"""
import logging
import random

# Total number of zones on the board. This should be an even number since the board is symmetrical.
NB_ZONES = 12

HALF_ZONES = int(NB_ZONES / 2)


class Game(object):
    """
    A game between two players A and B.

    The board is ordered this way:
         0  1  2  3  4  5
        11 10  9  8  7  6
    The following zones belong to the given users:
        A A A A A A
        B B B B B B
    """

    def __init__(self):
        self.zones = [0] * NB_ZONES

    def init_game(self):
        """
        Put the board in the initial state.

        The initial state is 5 seeds per zone, minus 3 picked in 3 different and random zones.
        """
        self.zones = [5] * NB_ZONES
        for zone_id in random.sample(population=range(NB_ZONES), k=3):
            self.zones[zone_id] -= 1
        logging.warning("Game initiated. Board state: %s", self.game_str())

    def game_str(self):
        """ Return the board state as a string """
        return self.board_str(self.zones)

    @staticmethod
    def board_str(zones):
        """ Return the given board state as a string """
        return "".join((
            "\n ",
            " ".join((str(nb) for nb in zones[0:HALF_ZONES])),
            "\n ",
            " ".join((str(nb) for nb in zones[HALF_ZONES:])),
        ))

    @property
    def board(self):
        """ Return the state of the board. """
        return self.zones.copy()

    def play(self, zone_id, player=None):
        """
        Play a given zone.

        Playing a zone means taking all the seeds from this zone, and then distributing one seed for
        each zone starting from the immediate next zone and ending when all the seeds have been
        distributed.
        """
        if player is None:
            player = 'A' if self.zone_belongs_to_player(zone_id, 'A') else 'B'
        elif player not in ['A', 'B']:
            raise ValueError("Player %s not recognized. Valid values are 'A' and 'B'." % player)
        if not self.zone_belongs_to_player(zone_id, player):
            raise ValueError("Cannot access this zone, you can only choose a zone if you side.")

        seeds_to_distribute = self.zones[zone_id]
        if seeds_to_distribute == 0:
            raise ValueError("This zone is already empty.")
        self.zones[zone_id] = 0
        receiving_zone = zone_id
        while seeds_to_distribute > 0:
            receiving_zone = (receiving_zone + 1) % NB_ZONES
            seeds_to_distribute -= 1
            self.zones[receiving_zone] += 1
        logging.warning("Player %s played zone %d", player, zone_id)
        # After a move, check if seeds can be removed
        self.auto_empty(end_zone=receiving_zone, player=player)

    def auto_empty(self, end_zone, player):
        """
        Empty the zones.

        Starting from the ending zone, remove the seeds from the zone if:
        * there is 2 or 3 seeds, and
        * the zone belongs to the player
        Whevener one of these conditions stops being true, stop emptying.
        """
        if not self.zone_belongs_to_player(end_zone, player):
            return

        if self.zones[end_zone] in [2, 3]:
            logging.warning("Emptying zone %d (%d seeds)", end_zone, self.zones[end_zone])
            self.zones[end_zone] = 0
            # Repeat from the preceding zone
            self.auto_empty((end_zone - 1) % NB_ZONES, player)

    def zone_belongs_to_player(self, zone_id, player):
        """ Return True if the zone belongs to the player """
        if player == 'A':
            return zone_id < HALF_ZONES
        if player == 'B':
            return zone_id >= HALF_ZONES
        return False

    def victory_reached(self):
        """ Return False if no player won, or the name ('A'/'B') of the winning player """
        if self.zones[:HALF_ZONES] == [0] * HALF_ZONES:
            return 'A'
        if self.zones[HALF_ZONES:] == [0] * HALF_ZONES:
            return 'B'

        # No winner yet
        return False


if __name__ == '__main__':
    game = Game()
    game.init_game()
    print(
        "View from player A:",
        game.board_str(game.board()),
    )
    game.play(0, 'B')
    print(
        "View from player A:",
        game.board_str(game.board()),
    )
