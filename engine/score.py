from collections import defaultdict
from itertools import combinations

from engine.rules import Rules
from models.card import Card


class Score:
    LAST_TO_PLAY = 1
    MAX_RUNNING_COUNT = 1

    HIS_HEELS = 2
    STARTER_JACK = 1
    FIFTEEN = 2
    PAIR = 2
    SEQUENCE = 1
    FLUSH = 1

    @staticmethod
    def starter_jack(cards, starter=None):
        if starter:
            starter_jack = Card(11, starter.color)
            if starter_jack in cards:
                return Score.STARTER_JACK

        return 0

    @staticmethod
    def fifteens(cards, starter=None):
        cards = cards + [starter] if starter else []

        card_numbers = defaultdict(int)
        for card in cards:
            card_numbers[card.number] += 1

        card_combinations = []
        for count in range(2, len(cards) + 1):
            card_combinations.extend(combinations(cards, count))

        score = 0
        for card_combination in card_combinations:
            if Rules.get_cards_value(card_combination) == 15:
                score += Score.FIFTEEN

        return score

    @staticmethod
    def pairs(cards, starter=None):
        cards = cards + ([starter] if starter else [])

        card_numbers = defaultdict(int)
        for card in cards:
            card_numbers[card.number] += 1

        score = 0
        for card_number, card_number_count in card_numbers.items():
            nb_pairs = (card_number_count - 1) * card_number_count / 2
            score += nb_pairs * Score.PAIR

        return score

    @staticmethod
    def sequences(cards, starter=None):
        cards = cards + [starter] if starter else []
        sorted_card_numbers = sorted(list(set([card.number for card in cards])))

        longest_sequence = []
        for count in range(Rules.MIN_SEQUENCE_LENGTH, len(sorted_card_numbers) + 1):
            sequences = combinations(sorted_card_numbers, count)
            for sequence in sequences:
                fake_cards = [Card(number, None) for number in sequence]
                if Rules.is_sequence(fake_cards) and len(sequence) > len(longest_sequence):
                    longest_sequence = sequence

        if len(longest_sequence) == 0:
            return 0

        card_numbers = defaultdict(int)
        for card in cards:
            card_numbers[card.number] += 1

        sequence_count = 1
        for number in longest_sequence:
            sequence_count *= card_numbers[number]

        return len(longest_sequence) * Score.SEQUENCE * sequence_count

    @staticmethod
    def flushes(cards, starter=None):
        cards_with_starter = cards + [starter] if starter else []
        if Rules.is_flush(cards_with_starter):
            return len(cards_with_starter) * Score.FLUSH

        if Rules.is_flush(cards):
            return len(cards) * Score.FLUSH

        return 0
