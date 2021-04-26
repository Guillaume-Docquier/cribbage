from collections import defaultdict

from models.card import Card
from models.deck import Deck


class CardStatistics:
    def __init__(self, deck: Deck):
        self.card_count = len(deck.cards)
        self.cards = defaultdict(int)
        self.card_numbers = defaultdict(int)
        self.card_colors = defaultdict(int)
        for card in deck.cards:
            self.cards[card] += 1
            self.card_numbers[card.number] += 1
            self.card_colors[card.color] += 1

    def remove_card(self, card):
        if self.cards[card] > 0:
            self.card_count -= 1
            self.cards[card] -= 1
            self.card_numbers[card.number] -= 1
            self.card_colors[card.color] -= 1

    def remove_cards(self, cards):
        for card in cards:
            self.remove_card(card)

    def probability_of_number(self, number):
        return self.card_numbers[number] / self.card_count

    def probability_of_color(self, color):
        return self.card_colors[color] / self.card_count

    def probability_of_card(self, card: Card):
        return self.cards[card] / self.card_count
