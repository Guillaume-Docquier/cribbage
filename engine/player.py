from abc import ABC, abstractmethod
from typing import List

from engine.rules import Rules
from models.card import Card


class Player(ABC):
    def __init__(self, name):
        self.name = name

        self.turn_order = None
        self.has_crib = False
        self.players = []
        self.initial_hand = []
        self.hand = []
        self.score = 0
        self.expected_score = None

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
        discarded = self.do_discard(self.hand.copy(), count)
        for discard in discarded:
            self.initial_hand.remove(discard)
            self.hand.remove(discard)

        return discarded

    @abstractmethod
    def do_discard(self, cards, count) -> List[Card]:
        pass

    def play(self, run, current_count) -> Card or None:
        playable_cards = self.get_playable_cards(current_count)
        if len(playable_cards) == 0:
            return self.go()

        played = self.do_play(playable_cards, run, current_count)
        self.hand.remove(played)

        return played

    @abstractmethod
    def do_play(self, cards, run, current_count) -> Card:
        pass

    def get_playable_cards(self, current_count) -> List[Card]:
        return [card for card in self.hand if Rules.get_card_value(card) + current_count <= Rules.MAX_RUNNING_COUNT]

    def go(self) -> None:
        self.say("No cards to play, go!")
        return None

    def say(self, what):
        print(f"[{self.name}] {what}")
