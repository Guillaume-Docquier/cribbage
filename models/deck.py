from .card import Card
from .color import Color
import random


class Deck:
    def __init__(self):
        self.cards = []
        for number in range(Card.MIN, Card.MAX + 1):
            for color in Color.tolist():
                self.cards.append(Card(number, color))

    def shuffle(self):
        for i in range(len(self.cards) - 1, 0, -1):
            j = random.randint(0, i + 1)
            self.cards[i], self.cards[j] = self.cards[j], self.cards[i]

    def draw(self):
        if len(self.cards) > 0:
            return self.cards.pop()

        return None

    def cut(self):
        if len(self.cards) > 0:
            pivot = random.randint(1, len(self.cards) - 2)
            self.cards = self.cards[pivot:] + self.cards[:pivot]

    def print(self):
        for card in self.cards:
            print(card)
