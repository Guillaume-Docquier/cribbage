from typing import List

from models.card import Card


class Rules:
    MAX_RUNNING_COUNT = 31

    MIN_SEQUENCE_LENGTH = 3
    MAX_SEQUENCE_LENGTH = 5
    MIN_FLUSH_LENGTH = 4

    @staticmethod
    def get_card_value(card: Card):
        return min(10, card.number)

    @staticmethod
    def get_cards_value(cards: List[Card]):
        return sum([Rules.get_card_value(card) for card in cards])

    @staticmethod
    def game_is_over(players, winning_score):
        for player in players:
            if player.score >= winning_score:
                return True

        return False

    @staticmethod
    def is_sequence(cards: List[Card]) -> bool:
        if len(cards) < Rules.MIN_SEQUENCE_LENGTH:
            return False

        sorted_card_numbers = sorted([card.number for card in cards])
        last_card_number = sorted_card_numbers[0]
        for card_number in sorted_card_numbers[1:]:
            if card_number != last_card_number + 1:
                return False

            last_card_number = card_number

        return True

    @staticmethod
    def is_flush(cards: List[Card]) -> bool:
        if len(cards) < Rules.MIN_FLUSH_LENGTH:
            return False

        colors = set([card.color for card in cards])
        if len(colors) > 1:
            return False

        return True
