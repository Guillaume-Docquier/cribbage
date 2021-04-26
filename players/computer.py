from itertools import combinations
from typing import List

from engine.player import Player
from engine.rules import Rules
from engine.scorer import Scorer
from models.card import Card
from models.deck import Deck
from players.card_statistics import CardStatistics


class Computer(Player):
    def __init__(self, name):
        super().__init__(f"Computer-{name}")

    def do_discard(self, count) -> List[Card]:
        deck = Deck.build_full_deck()
        deck.remove_cards(self.hand)

        card_statistics = CardStatistics(deck)
        possible_hands = combinations(self.hand, Rules.PLAYING_MAX_HAND_SIZE)
        best_possible_hand = None
        best_possible_potential = 0
        for possible_hand in possible_hands:
            potential = 0
            for starter in deck.cards:
                dummy = Computer("Dummy")
                Scorer.score_hand(dummy, list(possible_hand), starter, verbose=False)
                probability = card_statistics.probability_of_card(starter)
                potential += dummy.score * probability
                # TODO Consider points given to the crib

            if potential > best_possible_potential:
                best_possible_hand = possible_hand
                best_possible_potential = potential

        self.say(f"Hand {best_possible_hand} has the best potential of {best_possible_potential} points")

        discarded = []
        for card in self.hand:
            if card not in best_possible_hand:
                discarded.append(card)

        self.say(f"Discarding {discarded}")

        return discarded

    def do_play(self, run, current_count) -> Card or None:
        self.say(f"Run is {run}")
        self.say(f"Count is {current_count}")
        self.__show_hand()

        best_score = -1
        best_card = None
        # TODO Compute best card if equivalent. Biggest for now
        # TODO Consider that some cards cannot be played
        for card in sorted(self.hand, reverse=True):
            dummy = Computer("Dummy")
            Scorer.score_run(dummy, run + [card], current_count + Rules.get_card_value(card), verbose=False)
            if dummy.score > best_score:
                best_score = dummy.score
                best_card = card

        return best_card

    def __show_hand(self):
        self.say(f"Current hand")
        for index, card in enumerate(self.hand):
            self.say(f"\t{card}")
