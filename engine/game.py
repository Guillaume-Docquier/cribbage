import random
from typing import List, Deque
from collections import deque
from models.card import Card
from models.deck import Deck
from models.player import Player


class Game:
    PLAYING_MAX_HAND_SIZE = 4
    DEFAULT_WINNING_SCORE = 161
    SHORT_WINNING_SCORE = 61

    def __init__(self):
        self.players: Deque[Player] = deque()

        self.winning_score: int = self.DEFAULT_WINNING_SCORE
        self.deck: Deck or None = None
        self.crib: List[Card] = []
        self.starter: Card or None = None
        self.winner: Player or None = None

    def start(self, players: List[Player], short_game=False):
        random.shuffle(players)
        self.players = deque(players, maxlen=len(players))

        self.winning_score = self.SHORT_WINNING_SCORE if short_game else self.DEFAULT_WINNING_SCORE

        print(f"\nStarting game with players {players} with winning score {self.winning_score}")
        while not self.__game_is_over():
            print(f"\nNew round!")
            self.__change_dealer()
            self.__deal()
            self.__build_crib()
            self.__reveal_starter()
            self.__play()
            self.__score_hands()

    def __game_is_over(self):
        for player in self.players:
            if player.score >= self.winning_score:
                print(f"\nGame is over! {player.name} won the game with {player.score} points")
                print(f"Players: {list(self.players)}")
                return True

        return False

    def __change_dealer(self):
        print(f"\nChanging dealer...")
        self.players.append(self.players[0])

        players = list(self.players)
        turn_order = 0
        for player in self.players:
            has_crib = turn_order == len(players) - 1
            player.new_turn(turn_order, has_crib, players)
            turn_order += 1

        print(f"Dealer is now: {self.players[-1].name}")

    def __deal(self):
        print(f"\nDealing cards...")
        self.deck = Deck()
        self.deck.shuffle()
        self.crib = []

        nb_cards_in_play = self.PLAYING_MAX_HAND_SIZE * (len(self.players) + 1)
        nb_cards_to_deal = nb_cards_in_play // len(self.players)
        for i in range(nb_cards_to_deal):
            for player in self.players:
                player.deal(self.deck.draw())

        for i in range(nb_cards_in_play - nb_cards_to_deal):
            self.crib.append(self.deck.draw())

    def __build_crib(self):
        print(f"\nBuilding the crib...")
        for player in self.players:
            nb_cards_to_discard = len(player.cards) - self.PLAYING_MAX_HAND_SIZE
            print()
            self.crib.extend(player.discard(nb_cards_to_discard))

    def __reveal_starter(self):
        print(f"\nRevealing starter...")
        self.deck.cut()
        self.starter = self.deck.draw()
        print(f"Starter: {self.starter}")

    def __play(self):
        print(f"\nLet's play!")
        self.__show_scores()
        cards_to_play = len(self.players) * self.PLAYING_MAX_HAND_SIZE
        cards_played = 0
        current_turn = 0
        go_count = 0
        last_played: Player or None = None
        while cards_played < cards_to_play:
            running_count = 0
            if go_count == len(self.players):
                print(f"{last_played.name} pegs 1!")
                go_count = 0
                last_played = None

            while go_count != len(self.players):
                player = self.players[current_turn]
                print(f"\nCount is {running_count}, {player.name} to play")
                card_played = player.play(running_count)
                if card_played:
                    go_count = 0
                    last_played = player
                    cards_played += 1
                    running_count += min(10, card_played.number)
                    # TODO Score points
                    print(f"\n{player.name} played {card_played}!")
                    if self.__game_is_over():
                        return
                else:
                    go_count += 1
                    print(f"\n{player.name} says Go!")

                current_turn = (current_turn + 1) % len(self.players)

    def __score_hands(self):
        print(f"\nScoring hands...")
        # TODO
        self.__show_scores()

    def __show_scores(self):
        print(f"Scores are:")
        for player in self.players:
            print(f"\t{player.name}: {player.score} points")
