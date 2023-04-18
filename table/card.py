class Card:
    def __init__(self, rank, suit):
        self.suit = suit
        self.rank = rank
    def __str__(self):
        return f"{Card.rankToLabel(self.rank)} of {Card.suitToLabel(self.suit.value)}"
    def getString(self):
        return f"{Card.rankToChar(self.rank)}{Card.suitToChar(self.suit.value)}"
    @staticmethod
    def suitToLabel(suit):
        match suit:
            case 1:
                return "hearts"
            case 2:
                return "diamonds"
            case 3:
                return "clubs"
            case 4:
                return "spades"
            case _:
                return "unknown"
    @staticmethod
    def suitToChar(suit):
        match suit:
            case 1:
                return "H"
            case 2:
                return "D"
            case 3:
                return "C"
            case 4:
                return "S"
            case _:
                return "?"
    @staticmethod
    def rankToLabel(rank):
        match rank:
            case 0:
                return "unknown"
            case 1:
                return "ace"
            case 11:
                return "jack"
            case 12:
                return "queen"
            case 13:
                return "king"
            case _:
                return rank
    @staticmethod
    def rankToChar(rank):
        match rank:
            case 0:
                return "?"
            case 10:
                return "T"
            case 1:
                return "A"
            case 11:
                return "J"
            case 12:
                return "Q"
            case 13:
                return "K"
            case _:
                return rank
    @staticmethod
    def stringifyCardArray(cardArray):
        result = ""
        for card in cardArray:
            result+=card.getString()+","
        return result[:-1]
