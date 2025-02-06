import random
from src.classes.Card import Card

class Deck:
    def __init__(self, nb_of_decks = 5):
        self.nb_of_decks = nb_of_decks
        self.cards = []
        self.build()

    def build(self):
        suits = ['♥', '♦', '♣', '♠']
        values = [('2',2), ('3',3), ('4',4), ('5',5), ('6',6), ('7',7), ('8',8), ('9',9), ('10',10), ('J',10), ('Q',10), ('K',10), ('A',10)]
        for i in range(self.nb_of_decks):
            for suit in suits:
                for value in values:
                    self.cards.append(Card(suit, value[1], value[0]))

    def show(self):
        for card in self.cards:
            print(card)

    def shuffle(self):
        random.shuffle(self.cards)

    def draw_card(self):
        return self.cards.pop()

    def __str__(self):
        return f"Deck of {len(self.cards)} cards"