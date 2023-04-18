from table.card import Card
import random

class Deck:
    def __init__(self):
        self.cards = []
        self.generateDeck()
        self.shuffleDeck()
    def generateDeck(self):
        for rank in range(13):
            for value in range(4):
                self.cards.append(Card(rank+1,value+1))
    def shuffleDeck(self):
        random.shuffle(self.cards)