"""
Harness the IA bots and display stats about their performance.
"""

if __name__ == '__main__':
    from bots import RandomIA
    from game import Game

    game = Game()
    game.init_game()

    ia1 = RandomIA(game, 'A')
    ia2 = RandomIA(game, 'B')

    step = 1
    while not game.victory_reached():
        player_ia = ia1 if step % 2 == 0 else ia2
        zone_played = player_ia.choose_absolute_move()
        game.play(zone_id=zone_played, player=player_ia.player_name)
        print(f"Step {step}, player {player_ia.player_name} ({player_ia.strategy}) played {zone_played}")
        step += 1
    winner = game.victory_reached()
    print(f"Game finished, player {winner} won.")
