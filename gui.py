import gi
from gi.repository import Gtk

gi.require_version('Gtk', '3.0')

GAME_NAME = "Aveijieux"


class BoardWindow(Gtk.Window):
    def __init__(self, game):
        self.game = game
        Gtk.Window.__init__(self, title=GAME_NAME)

        self.boxA = Gtk.Box(spacing=6)
        self.boxB = Gtk.Box(spacing=6)
        self.board = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)
        self.board.pack_start(self.boxA, True, True, 0)
        self.board.pack_start(self.boxB, True, True, 0)
        self.add(self.board)

        # Draw board
        self.buttons = [None] * 12
        for id, zone in enumerate(game.board):
            self.buttons[id] = Gtk.Button(label=str(zone))
            self.buttons[id].connect("clicked", self.on_zone_clicked_call(id))
            if id < 6:
                self.boxA.pack_start(self.buttons[id], True, True, 0)
            else:
                self.boxB.pack_end(self.buttons[id], True, True, 0)

    def on_zone_clicked_call(self, zone_id):
        def click(btn_self):
            print(f"Zone #{zone_id} clicked.")
            self.game.play(zone_id)
            # Update the board
            for id, zone in enumerate(game.board):
                self.buttons[id].set_label(str(zone))

            winner = game.victory_reached()
            if winner:
                print(f"Player {winner} won! End of the game.")

        return click


if __name__ == '__main__':
    from game import Game
    game = Game()
    game.init_game()

    win = BoardWindow(game)
    win.connect("destroy", Gtk.main_quit)
    win.show_all()
    Gtk.main()
