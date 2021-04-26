from abc import ABC, abstractmethod
from typing import List

from .card import Card


class Player(ABC):
    def __init__(self, name):
        self.name = name

        self.turn_order = None
        self.has_crib = False
        self.players = []
        self.cards = []
        self.score = 0

    def __repr__(self):
        return f"{self.name}.{self.score}.{self.cards}"

    def new_turn(self, turn_order, has_crib, players):
        self.turn_order = turn_order
        self.has_crib = has_crib
        self.players = players

    def deal(self, card):
        self.cards.append(card)

    def discard(self, count) -> List[Card]:
        discarded = self.do_discard(count)
        for discard in discarded:
            self.cards.remove(discard)

        return discarded

    @abstractmethod
    def do_discard(self, count) -> List[Card]:
        pass

    def play(self, current_count) -> Card or None:
        played = self.do_play(current_count)
        if played:
            self.cards.remove(played)

        return played

    @abstractmethod
    def do_play(self, current_count) -> Card or None:
        pass

    def score(self, starter):
        # TODO
        pass
