from typing import List

from engine.rules import Rules
from models.card import Card
from engine.player import Player


class Human(Player):
    def do_discard(self, count) -> List[Card]:
        self.__show_hand()
        
        while True:
            self.say(f"Choose {count} card(s) to discard by entering their index (0 to {len(self.hand) - 1}) on one line separated by a space")
            try:
                discard_indices = list(set(map(int, input().split(" "))))
                if len(discard_indices) == count and all(discard_index < len(self.hand) for discard_index in discard_indices):
                    discarded = []
                    for index in discard_indices:
                        discarded.append(self.hand[index])

                    self.say(f"Discarded {discarded}")

                    return discarded
                else:
                    self.__invalid_choice()
            except ValueError:
                self.__invalid_choice()

    def do_play(self, run, current_count) -> Card or None:
        self.say(f"Run is {run}")
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
