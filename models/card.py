from models.color import Color

figures = {
    1: "A",
    11: "J",
    12: "Q",
    13: "K"
}

color_index = {
    Color.CLUBS: 0,
    Color.HEARTS: 1,
    Color.DIAMONDS: 2,
    Color.SPADES: 3
}


class Card:
    MIN = 1
    MAX = 13

    def __init__(self, number, color):
        self.number = number
        self.color = color

    def __repr__(self):
        return f"{figures[self.number] if self.number in figures else self.number}.{self.color}"

    def __hash__(self):
        return self.number * len(color_index) + color_index[self.color]

    def __eq__(self, other):
        return (self.number, self.color) == (other.number, other.color)

    def __ne__(self, other):
        return (self.number, self.color) != (other.number, other.color)

    def __lt__(self, other):
        return (self.number, self.color) < (other.number, other.color)

    def __le__(self, other):
        return (self.number, self.color) <= (other.number, other.color)

    def __gt__(self, other):
        return (self.number, self.color) > (other.number, other.color)

    def __ge__(self, other):
        return (self.number, self.color) >= (other.number, other.color)
