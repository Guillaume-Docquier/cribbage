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
        self.card_statistics = None

    def do_discard(self, cards, count) -> List[Card]:
        deck = Deck.build_full_deck()
        deck.remove_cards(cards)
        self.card_statistics = CardStatistics(Deck.build_full_deck())

        possible_hands = combinations(cards, Rules.PLAYING_MAX_HAND_SIZE)

        best_possible_hand = None
        best_possible_potential = 0
        for possible_hand in possible_hands:
            potential = 0
            for starter in deck.cards:
                dummy = Computer("Dummy")
                Scorer.score_hand(dummy, list(possible_hand), starter, verbose=False)
                probability = self.card_statistics.probability_of_card(starter)
                potential += dummy.score * probability
                # TODO Consider points given to the crib

            if potential > best_possible_potential:
                best_possible_hand = possible_hand
                best_possible_potential = potential

        self.say(f"Hand {best_possible_hand} has the best potential of {best_possible_potential:.3f} points")

        discarded = []
        for card in cards:
            if card not in best_possible_hand:
                discarded.append(card)

        self.say(f"Discarding {discarded}")

        return discarded

    def do_play(self, cards, run, current_count) -> Card or None:
        self.say(f"Run is {run}")
        self.say(f"Count is {current_count}")
        self.__show_playable_cards(cards)

        self.card_statistics.remove_cards(cards)
        self.card_statistics.remove_cards(run)

        best_score = -1
        best_card = None
        # TODO Compute best card if equivalent. Biggest for now
        for card in sorted(cards, reverse=True):
            dummy = Computer("Dummy")
            Scorer.score_run(dummy, run + [card], current_count + Rules.get_card_value(card), verbose=False)
            if dummy.score > best_score:
                best_score = dummy.score
                best_card = card

        return best_card

    def __show_playable_cards(self, cards):
        self.say(f"Cards available")
        for index, card in enumerate(cards):
            self.say(f"\t{card}")
