from models.deck import Deck

if __name__ == "__main__":
    print("Initial deck")
    deck = Deck()
    deck.print()

    print("\nCut deck")
    deck.cut()
    deck.print()

    print("\nShuffled deck")
    deck.shuffle()
    deck.print()

    for i in range(3):
        print("\nDraw")
        card = deck.draw()
        print(card)
