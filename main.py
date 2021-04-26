from engine.game import Game
from players.computer import Computer
from players.human import Human

if __name__ == "__main__":
    players = [
        Computer("Guillaume"),
        Computer("Manfred"),
        Computer("Charles")
    ]

    game = Game()
    game.start(players)
