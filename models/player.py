from abc import ABC, abstractmethod
from typing import List

from engine.rules import Rules
from .card import Card


class Player(ABC):
    def __init__(self, name):
        self.name = name

        self.turn_order = None
        self.has_crib = False
        self.players = []
        self.initial_hand = []
        self.hand = []
        self.score = 0

    def __repr__(self):
        return f"{self.name}.{self.score}.{self.hand}"

    def new_turn(self, turn_order, has_crib, players):
        self.turn_order = turn_order
        self.has_crib = has_crib
        self.players = players

        self.initial_hand = []
        self.hand = []

    def deal(self, card):
        self.initial_hand.append(card)
        self.hand.append(card)

    def discard(self, count) -> List[Card]:
        discarded = self.do_discard(count)
        for discard in discarded:
            self.initial_hand.remove(discard)
            self.hand.remove(discard)

        return discarded

    @abstractmethod
    def do_discard(self, count) -> List[Card]:
        pass

    def play(self, current_count) -> Card or None:
        if len(self.hand) == 0 or current_count + min([Rules.get_card_value(card) for card in self.hand]) > Rules.MAX_RUNNING_COUNT:
            return self.go()

        played = self.do_play(current_count)
        self.hand.remove(played)

        return played

    @abstractmethod
    def do_play(self, current_count) -> Card:
        pass

    def go(self) -> None:
        self.say("No cards to play, go!")
        return None

    def say(self, what):
        print(f"[{self.name}] {what}")
