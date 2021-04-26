from collections import defaultdict

from models.card import Card
from models.deck import Deck


class CardStatistics:
    def __init__(self, deck: Deck):
        self.deck = deck
        self.card_numbers = defaultdict(int)
        self.card_colors = defaultdict(int)
        for card in deck.cards:
            self.card_numbers[card.number] += 1
            self.card_colors[card.color] += 1

    def probability_of_number(self, number):
        return self.card_numbers[number] / len(self.deck.cards)

    def probability_of_color(self, color):
        return self.card_colors[color] / len(self.deck.cards)

    def probability_of_card(self, card: Card):
        if card not in self.deck.cards:
            return 0

        return 1 / len(self.deck.cards)
