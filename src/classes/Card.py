class Card:
    def __init__(self, suit, value, name):
        self.suit = suit
        self.value = value
        self.name = name

    def to_ascii(self):
#        hearts = "♥"
#        diamonds = "♦"
#        clubs = "♣"
#        spades = "♠"
        return f"""
        ┌─────────┐
        │ {self.value}       │
        │         │
        │         │
        │    {self.suit}    │
        │         │
        │         │
        │       {self.value} │
        └─────────┘
        """
    
    def to_print(self):
        return f"{self.value} of {self.suit}"

    def __str__(self):
        return f"{self.value} of {self.suit}"