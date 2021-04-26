from typing import List

from .card import Card
from .player import Player


class Human(Player):
    def do_discard(self, count) -> List[Card]:
        self.__show_hand()
        
        while True:
            self.__say(f"Choose {count} card(s) to discard by entering their index (0 to {len(self.cards) - 1}) on one line separated by a space")
            try:
                discard_indices = list(set(map(int, input().split(" "))))
                if len(discard_indices) == count and all(discard_index < len(self.cards) for discard_index in discard_indices):
                    discarded = []
                    for index in discard_indices:
                        discarded.append(self.cards[index])

                    self.__say(f"Discarded {discarded}")

                    return discarded
                else:
                    self.__say(f"Invalid choice")
            except ValueError:
                self.__say(f"Invalid choice")

    def do_play(self, current_count) -> Card or None:
        self.__say(f"Count is {current_count}")
        self.__show_hand()

        while True:
            self.__say(f"Choose a card to play by entering its index (0 to {len(self.cards) - 1}), or 'Go' if impossible")
            choice = input()
            if choice == "Go":
                return None

            try:
                choice = int(choice)
                if choice < len(self.cards):
                    card_played = self.cards[int(choice)]
                    self.__say(f"Played {card_played}")

                    return card_played
                else:
                    self.__say(f"Invalid choice")
            except ValueError:
                self.__say(f"Invalid choice")

    def __say(self, what):
        print(f"[{self.name}] {what}")

    def __show_hand(self):
        self.__say(f"Current hand")
        for index, card in enumerate(self.cards):
            self.__say(f"\t{index} -> {card}")
