from itertools import combinations
from typing import List

from engine.player import Player
from engine.rules import Rules
from engine.scorer import Scorer
from models.card import Card
from models.deck import Deck
from players.card_statistics import CardStatistics


class Computer(Player):
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

    # TODO Auto-play
    def do_play(self, current_count) -> Card or None:
        self.say(f"Count is {current_count}")
        self.__show_hand()

        while True:
            self.say(f"Choose a card to play by entering its index (0 to {len(self.hand) - 1})")
            try:
                choice = int(input())
                if choice < len(self.hand):
                    card_played = self.hand[int(choice)]
                    self.say(f"Played {card_played}")

                    if Rules.get_card_value(card_played) + current_count <= Rules.MAX_RUNNING_COUNT:
                        return card_played
                    else:
                        self.__invalid_choice()
                else:
                    self.__invalid_choice()
            except ValueError:
                self.__invalid_choice()

    def __show_hand(self):
        self.say(f"Current hand")
        for index, card in enumerate(self.hand):
            self.say(f"\t{index} -> {card}")

    def __invalid_choice(self):
        self.say(f"Invalid choice")
