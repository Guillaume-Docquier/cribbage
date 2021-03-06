from typing import List

from engine.rules import Rules
from engine.score import Score
from models.card import Card
from engine.player import Player


class Scorer:
    SCORING_METHODS = [
        ("starter jack", Score.starter_jack),
        ("fifteens", Score.fifteens),
        ("pairs", Score.pairs),
        ("sequences", Score.sequences),
        ("flushes", Score.flushes),
    ]

    @staticmethod
    def score_his_heels(player: Player, starter: Card):
        if starter.number == 11:
            print(f"{player.name} was the dealer, revealed a jack and scores {Score.HIS_HEELS}!")
            player.score += Score.HIS_HEELS

    @staticmethod
    def score_last_to_play(player: Player, running_count: int):
        print(f"{player.name} was last to play and pegs {Score.LAST_TO_PLAY}!")
        player.score += Score.LAST_TO_PLAY
        if running_count == Rules.MAX_RUNNING_COUNT:
            print(f"{player.name} hit {Rules.MAX_RUNNING_COUNT} and pegs {Score.MAX_RUNNING_COUNT} more!")
            player.score += Score.MAX_RUNNING_COUNT

    @staticmethod
    def score_run(player: Player, run: List[Card], running_count: int, verbose=True):
        fifteen_score = 0
        if running_count == 15:
            fifteen_score = Score.FIFTEEN
            if verbose:
                print(f"{player.name} scored {fifteen_score} for hitting 15!")

        pairs_score = 0
        max_pairs_sequence_length = min(4, len(run))
        for count in range(max_pairs_sequence_length, 2 - 1, -1):
            cards_considered = run[-count:]
            card_variety = len(set([card.number for card in cards_considered]))
            if card_variety == 1:
                pairs_score = Score.pairs(cards_considered)
                if verbose:
                    print(f"{player.name} scored {pairs_score} for pairs!")
                break

        sequence_score = 0
        max_sequence_length = min(Rules.MAX_SEQUENCE_LENGTH, len(run))
        for count in range(max_sequence_length, Rules.MIN_SEQUENCE_LENGTH - 1, -1):
            cards_considered = run[-count:]
            if Rules.is_sequence(cards_considered):
                sequence_score = len(cards_considered) * Score.SEQUENCE
                if verbose:
                    print(f"{player.name} scored {sequence_score} for sequence!")
                break

        player.score += (fifteen_score + pairs_score + sequence_score)

    @staticmethod
    def score_hand(player: Player, hand: List[Card], starter: Card, verbose=True):
        if verbose:
            print(f"Scoring for {player.name}")
            print(f"Starter is {starter}")
            print(f"Hand is")
            for index, card in enumerate(hand):
                print(f"\t{card}")

        total_score = 0
        for scoring_name, scoring_func in Scorer.SCORING_METHODS:
            score = scoring_func(hand, starter)
            if verbose:
                print(f"{player.name} scored {score} for {scoring_name}")

            total_score += score

        if verbose:
            print(f"{player.name} scored a total of {total_score} points (expected {player.expected_score})")

        player.score += total_score
