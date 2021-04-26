from models.player import Player


class Scores:
    GO = 1
    RUN = 2


class Scorer:
    @staticmethod
    def go(player: Player):
        score = Scores.GO
        print(f"{player.name} was last to play and pegs {score}!")
        player.score += score

    @staticmethod
    def run(player: Player):
        score = Scores.RUN
        print(f"{player.name} hit 31 and pegs {score}!")  # TODO 31
        player.score += score
