from typing import List

from .card import Card
from .color import Color
import random


class Deck:
    def __init__(self, cards=None):
        self.cards = cards if cards else []

    @staticmethod
    def build_full_deck():
        cards = []
        for number in range(Card.MIN, Card.MAX + 1):
            for color in Color.tolist():
                cards.append(Card(number, color))

        return Deck(cards)

    def shuffle(self):
        random.shuffle(self.cards)

    def draw(self):
        if len(self.cards) > 0:
            return self.cards.pop()

        return None

    def cut(self):
        if len(self.cards) > 0:
            pivot = random.randint(1, len(self.cards) - 2)
            self.cards = self.cards[pivot:] + self.cards[:pivot]

    def remove_cards(self, cards: List[Card]):
        for card in cards:
            if card not in self.cards:
                stop = 0

            self.cards.remove(card)

    def print(self):
        for card in self.cards:
            print(card)
