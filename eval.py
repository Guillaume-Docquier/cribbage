from engine.scorer import Scorer
from models.card import Card
from players.computer import Computer
from models.color import Color

if __name__ == "__main__":
    player = Computer("evaluator")
    player.has_crib = True
    crib_is_known = False

    crib_player = Computer("crib")

    player.deal(Card(2, Color.HEARTS))
    player.deal(Card(6, Color.HEARTS))
    player.deal(Card(6, Color.SPADES))
    player.deal(Card(8, Color.DIAMONDS))
    player.deal(Card(10, Color.SPADES))
    player.deal(Card(11, Color.DIAMONDS))

    starter = Card(2, Color.DIAMONDS)

    discarded = player.discard(2)

    crib = discarded + [Card(2, Color.HEARTS), Card(8, Color.DIAMONDS)]
    crib.sort(key=lambda x: x.number)

    Scorer.score_hand(player, player.initial_hand, starter, verbose=False)

    if crib_is_known:
        Scorer.score_hand(crib_player, crib, starter, verbose=False)

    if not player.has_crib:
        crib_player.score *= 1

    print("")
    print(f"Starter was {starter}")
    if crib_is_known:
        print(f"Crib was {crib}")
    print(f"With the best hand, you would have scored {player.score + crib_player.score} ({player.score} hand, {crib_player.score} crib)")
