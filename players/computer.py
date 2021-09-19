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
        self.card_statistics = CardStatistics(deck)

        cards.sort(key=lambda x: x.number)
        possible_hands = combinations(cards, Rules.PLAYING_MAX_HAND_SIZE)

        potentials = []
        for possible_hand in possible_hands:
            potential = 0
            crib_potential = 0
            for starter in deck.cards:
                dummy = Computer("Dummy")
                Scorer.score_hand(dummy, list(possible_hand), starter, verbose=False)
                probability = self.card_statistics.probability_of_card(starter)
                potential += dummy.score * probability
                discarded = [card for card in cards if card not in possible_hand]
                crib_potential += self.__compute_crib_potential(discarded, starter, deck) * probability

            if not self.has_crib:
                crib_potential *= -1

            potentials.append((possible_hand, potential, crib_potential))

        potentials.sort(key=lambda x: x[1] + x[2], reverse=True)

        self.say(f"Cards: {cards}")
        self.say("Top 5 hands:")
        for (hand, score, crib_score) in potentials[:5]:
            self.say(f"\t{hand}: {score + crib_score:.3f} points ({score:.3f} hand, {crib_score:.3f} crib)")
        self.say("")

        best_possible_hand, best_potential_score, crib_potential = potentials[0]
        self.expected_score = best_potential_score
        discarded = [card for card in cards if card not in best_possible_hand]

        self.say(f"Hand {best_possible_hand} has the best potential of {best_potential_score + crib_potential:.3f} points ({best_potential_score:.3f} hand, {crib_potential:.3f} crib)")
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

    def __compute_crib_potential(self, discarded, starter, deck) -> int:
        self.card_statistics.remove_card(starter)

        possible_other_cards = combinations(deck.cards, Rules.PLAYING_MAX_HAND_SIZE - 1 - len(discarded))
        potential = 0
        for other_cards in possible_other_cards:
            probability = 1
            for card in other_cards:
                # TODO Not all cards have the same chance of being discarded by other players since they will keep good cards or pairs
                probability *= self.card_statistics.probability_of_card(card)

            dummy = Computer("Dummy")
            Scorer.score_hand(dummy, discarded + list(other_cards), starter, verbose=False)
            potential += dummy.score * probability

        self.card_statistics.add_card(starter)

        return potential

    def __show_playable_cards(self, cards):
        self.say(f"Cards available")
        for index, card in enumerate(cards):
            self.say(f"\t{card}")
