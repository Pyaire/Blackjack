class Card:
    """ 
    A class to represent a playing card.
    """
    def __init__(self, suit: str, value: int, name: str):
        """
        __init__ is a method that initializes the Card class.

        Parameters
        ----------
        suit : str
            This is the suit of the card ('♥', '♦', '♣', '♠').
        value : int
            This is the value of the card (between 2 and 10).
        name : str
            This is the name of the card (in [2,3,4,5,6,7,8,9,10,J,Q,K,A]).
        """
        self.suit = suit
        self.value = value
        self.name = name

    def to_ascii(self):
        """
        to_ascii is a method that returns the ASCII representation of the card.
        """
        return f"""
        ┌─────────┐
        │ {self.name}       │
        │         │
        │         │
        │    {self.suit}    │
        │         │
        │         │
        │       {self.name} │
        └─────────┘
        """
    
    def to_print(self) -> str:
        """
        to_print is a method that returns the string representation of the card.

        Returns
        -------
        str
            The string representation of the card.
        """
        return f"{self.value} of {self.suit}"

    def __str__(self) -> str:
        """
        __str__ is a method that returns the string representation of the card.

        Returns
        -------
        str
            The string representation of the card.
        """
        return f"{self.value} of {self.suit}"