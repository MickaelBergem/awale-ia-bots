from unittest import TestCase

from .game import Game


class GameTest(TestCase):

    def test_init(self):
        """ init_game should fill the right number of seeds """
        game = Game()
        game.init_game()
        self.assertEqual(sum(game.board), (5 * 12) - 3)
        for zone in game.board:
            self.assertTrue(zone >= 4)
            self.assertTrue(zone <= 5)

    def test_board_players(self):
        """
        The board and player-relative methods should be consistent.

        From the docs:

            The board is ordered this way:
                 0  1  2  3  4  5
                11 10  9  8  7  6
            The following zones belong to the given users:
                A A A A A A
                B B B B B B
        """
        game = Game()
        game.init_game()
        self.assertTrue(game.zone_belongs_to_player(0, 'A'))

        self.assertTrue(game.zone_belongs_to_player(5, 'A'))
        self.assertFalse(game.zone_belongs_to_player(5, 'B'))

        self.assertTrue(game.zone_belongs_to_player(6, 'B'))
        self.assertFalse(game.zone_belongs_to_player(6, 'A'))

        self.assertTrue(game.zone_belongs_to_player(11, 'B'))

        self.assertEqual(game.victory_reached(), False)
        game.zones = [1] * 6 + [0] * 6
        self.assertEqual(game.victory_reached(), 'B')

    def test_rules(self):
        """ Gameplay check """
        game = Game()
        # Force zone configuration
        game.zones = [5, 4, 3, 5, 1, 0] + [2, 3, 4, 5, 6, 7]
        game.play(7, 'B')
        self.assertEqual(
            game.zones,
            [5, 4, 3, 5, 1, 0] + [2, 0, 5, 6, 7, 7],
        )
        game.play(3, 'A')
        self.assertEqual(
            game.zones,
            [5, 4, 3, 0, 2, 1] + [3, 1, 6, 6, 7, 7],
        )
        game.play(11, 'B')
        self.assertEqual(
            game.zones,
            [6, 5, 4, 1, 3, 2] + [4, 1, 6, 6, 7, 0],
        )

    def test_autoempty(self):
        """ Check the auto_empty mechanism """
        game = Game()
        game.zones = [1] * 12
        game.play(3, 'A')
        self.assertEqual(game.zones[0:6], [1, 1, 1, 0, 0, 1])

        game.zones = [1] * 12
        game.play(5, 'A')
        self.assertEqual(game.zones, [1, 1, 1, 1, 1, 0, 2, 1, 1, 1, 1, 1])

    def test_victory(self):
        """ Check the victory_reached method """
        game = Game()
        # Force zone configuration
        game.zones = [1] * 6 + [5, 1, 1, 1, 1, 1]
        self.assertFalse(game.victory_reached())
        game.play(0, 'A')
        self.assertFalse(game.victory_reached())
        game.play(6, 'B')
        self.assertTrue(game.victory_reached())
