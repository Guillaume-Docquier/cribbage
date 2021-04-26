from engine.game import Game
from models.human import Human

if __name__ == "__main__":
    players = [
        Human("Guillaume"),
        Human("Manfred"),
        Human("Charles")
    ]

    game = Game()
    game.start(players)
