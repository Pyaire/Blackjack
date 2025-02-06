import random
from src.classes.Card import Card

class Deck:
    """
    Deck is a class that represents a deck of cards in a game of blackjack with a certain number of decks
    """
    def __init__(self, nb_of_decks = 5):
        """
        __init__ is a method that initializes the Deck object

        Parameters
        ----------
        nb_of_decks : int, optional
            Number of card's deck, by default 5
        """
        self.nb_of_decks = nb_of_decks
        self.cards = []
        self.build()

    def build(self):
        """
        build is a method that builds the deck of cards
        """
        suits = ['♥', '♦', '♣', '♠']
        values = [('2',2), ('3',3), ('4',4), ('5',5), ('6',6), ('7',7), ('8',8), ('9',9), ('10',10), ('J',10), ('Q',10), ('K',10), ('A',10)]
        for i in range(self.nb_of_decks):
            for suit in suits:
                for value in values:
                    self.cards.append(Card(suit, value[1], value[0]))

    def shuffle(self):
        """
        shuffle is a method that shuffles the deck of cards
        """
        random.shuffle(self.cards)

    def draw_card(self) -> Card:
        """
        draw_card is a method that draws a card from the deck

        Returns
        -------
        Card
            The card drawn from the deck
        """
        return self.cards.pop()

    def __str__(self) -> str:
        """
        __str__ is a method that returns the string representation of the deck

        Returns
        -------
        str
            The string representation of the deck
        """
        return f"Deck of {len(self.cards)} cards"