from typing import List

from engine.rules import Rules
from models.card import Card
from engine.player import Player


class Human(Player):
    def do_discard(self, cards, count) -> List[Card]:
        self.__show_playable_cards(cards)
        
        while True:
            self.say(f"Choose {count} card(s) to discard by entering their index (0 to {len(cards) - 1}) on one line separated by a space")
            try:
                discard_indices = list(set(map(int, input().split(" "))))
                if len(discard_indices) == count and all(discard_index < len(cards) for discard_index in discard_indices):
                    discarded = []
                    for index in discard_indices:
                        discarded.append(cards[index])

                    self.say(f"Discarded {discarded}")

                    return discarded
                else:
                    self.__invalid_choice()
            except ValueError:
                self.__invalid_choice()

    def do_play(self, cards, run, current_count) -> Card or None:
        self.say(f"Run is {run}")
        self.say(f"Count is {current_count}")
        self.__show_playable_cards(cards)

        while True:
            self.say(f"Choose a card to play by entering its index (0 to {len(cards) - 1})")
            try:
                choice = int(input())
                if choice < len(cards):
                    card_played = cards[int(choice)]
                    self.say(f"Played {card_played}")

                    if Rules.get_card_value(card_played) + current_count <= Rules.MAX_RUNNING_COUNT:
                        return card_played
                    else:
                        self.__invalid_choice()
                else:
                    self.__invalid_choice()
            except ValueError:
                self.__invalid_choice()

    def __show_playable_cards(self, cards):
        self.say(f"Cards available")
        for index, card in enumerate(cards):
            self.say(f"\t{index} -> {card}")

    def __invalid_choice(self):
        self.say(f"Invalid choice")
