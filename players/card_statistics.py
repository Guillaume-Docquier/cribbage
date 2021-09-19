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

    def remove_card(self, card_to_remove):
        if self.cards[card_to_remove] > 0:
            self.card_count -= 1
            self.cards[card_to_remove] -= 1
            self.card_numbers[card_to_remove.number] -= 1
            self.card_colors[card_to_remove.color] -= 1

    def remove_cards(self, cards_to_remove):
        for card_to_remove in cards_to_remove:
            self.remove_card(card_to_remove)

    def add_card(self, card_to_add):
        self.card_count += 1
        self.cards[card_to_add] += 1
        self.card_numbers[card_to_add.number] += 1
        self.card_colors[card_to_add.color] += 1

    def add_cards(self, cards_to_add):
        for card_to_add in cards_to_add:
            self.add_card(card_to_add)

    def probability_of_number(self, number):
        return self.card_numbers[number] / self.card_count

    def probability_of_color(self, color):
        return self.card_colors[color] / self.card_count

    def probability_of_card(self, card: Card):
        return self.cards[card] / self.card_count
