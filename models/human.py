from typing import List

from .card import Card
from .player import Player


class Human(Player):
    def do_discard(self, count) -> List[Card]:
        self.__show_hand()
        
        while True:
            self.say(f"Choose {count} card(s) to discard by entering their index (0 to {len(self.cards) - 1}) on one line separated by a space")
            try:
                discard_indices = list(set(map(int, input().split(" "))))
                if len(discard_indices) == count and all(discard_index < len(self.cards) for discard_index in discard_indices):
                    discarded = []
                    for index in discard_indices:
                        discarded.append(self.cards[index])

                    self.say(f"Discarded {discarded}")

                    return discarded
                else:
                    self.say(f"Invalid choice")
            except ValueError:
                self.say(f"Invalid choice")

    def do_play(self, current_count) -> Card or None:
        self.say(f"Count is {current_count}")
        self.__show_hand()

        while True:
            self.say(f"Choose a card to play by entering its index (0 to {len(self.cards) - 1})")
            try:
                choice = int(input())
                if choice < len(self.cards):
                    card_played = self.cards[int(choice)]
                    self.say(f"Played {card_played}")

                    return card_played
                else:
                    self.say(f"Invalid choice")
            except ValueError:
                self.say(f"Invalid choice")

    def __show_hand(self):
        self.say(f"Current hand")
        for index, card in enumerate(self.cards):
            self.say(f"\t{index} -> {card}")
