symbols = {
    1: "A",
    11: "J",
    12: "Q",
    13: "K"
}


class Card:
    MIN = 1
    MAX = 13

    def __init__(self, number, color):
        self.number = number
        self.color = color

    def __repr__(self):
        return f"{symbols[self.number] if self.number in symbols else self.number}.{self.color}"

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
