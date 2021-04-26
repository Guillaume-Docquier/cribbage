from engine.player import Player
from .rules import Rules
from .scorer import Scorer
from typing import Callable


class Run:
    def __init__(self, players, nb_cards_to_play):
        self.players = players
        self.players_playing = players.copy()
        self.nb_cards_to_play = nb_cards_to_play

        self.cards_played = 0
        self.current_turn = 0
        self.last_played: Player or None = None

    def start(self, is_game_over: Callable[[], bool]):
        self.__initialize_turn()

        running_count = 0
        cards_in_the_run = []
        while len(self.players_playing) > 0 and running_count < Rules.MAX_RUNNING_COUNT and not is_game_over():
            player = self.players_playing[self.current_turn]
            print(f"\nCount is {running_count}, {player.name} to play")
            card_played = player.play(cards_in_the_run, running_count)
            if card_played:
                cards_in_the_run.append(card_played)
                self.last_played = player
                self.cards_played += 1
                running_count += Rules.get_card_value(card_played)

                print(f"\n{player.name} played {card_played}!")
                Scorer.score_run(player, cards_in_the_run, running_count)

                self.__increment_turn()
            else:
                self.__remove_player(player)
                print(f"\n{player.name} says Go!")

        Scorer.last_to_play(self.last_played, running_count)

    def is_over(self):
        return self.cards_played == self.nb_cards_to_play

    def __initialize_turn(self):
        if self.last_played:
            self.players_playing = self.players.copy()
            self.current_turn = self.players_playing.index(self.last_played)
            self.__increment_turn()
            self.last_played = None

    def __increment_turn(self):
        self.current_turn = (self.current_turn + 1) % len(self.players_playing)

    def __remove_player(self, player):
        self.players_playing.remove(player)
        if len(self.players_playing) > 0:
            self.current_turn = self.current_turn % len(self.players_playing)
