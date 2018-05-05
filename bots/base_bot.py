class BaseBot(object):
    """
    IA bot. A bot always assume she is playing as Player A.

    The board is ordered this way:
         0  1  2  3  4  5
        11 10  9  8  7  6
    The following zones belong to the given users:
        A A A A A A
        B B B B B B
    """

    strategy = None

    def __init__(self, game, player_name):
        self.game = game
        self.player_name = player_name

    def choose_move(self):
        """ Return the zone_id to play """
        raise NotImplementedError()

    def relative_board(self):
        """ Return the board representation so that we are Player A """
        board = self.game.board
        if self.player_name == 'A':
            return board
        # Revert the board
        return board[6:] + board[:6]

    def choose_absolute_move(self):
        """ Return the absolute zone ID """
        move = self.choose_move()
        if self.player_name == 'A':
            return move
        # Player B, revert the IDs
        return (move + 6) % 12
