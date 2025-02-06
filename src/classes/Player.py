class Player:
    """
    Player is a class that represents a player in the game
    (DAO exists in the same folder)
    """

    def __init__(self, name: str, wallet: int, games_played: int, games_won: int, nb_bankrupt: int):
        """
        __init__ is a method that initializes the Player class.

        Parameters
        ----------
        name : str
            The name of the player
        wallet : int
            The amount of money the player has
        games_played : int
            The number of games the player has played
        games_won : int
            The number of games the player has won
        nb_bankrupt : int
            The number of times the player has gone bankrupt (money = 0)
        """
        self.name = name
        self.wallet = wallet
        self.games_played = games_played
        self.games_won = games_won
        self.nb_bankrupt = nb_bankrupt

    @classmethod
    def from_dict(cls, dict):
        """
        from_dict is a class method that creates a Player object from a dictionary

        Parameters
        ----------
        dict : dict
            A dictionary containing the attributes of the Player object

        Returns
        -------
        Player
            A Player object created from the dictionary

        Examples
        --------
        >>> dict = {"name": "Justin", "wallet": 20000, "games_played": 0, "games_won": 0, "nb_bankrupt": 0}
        >>> player = Player.from_dict(dict)
        """
        return cls(dict["name"], dict["wallet"], dict["games_played"], dict["games_won"], dict["nb_bankrupt"])

    def get_wallet(self) -> int:
        """
        get_wallet is a method that returns the wallet of the player

        Returns
        -------
        int
            The amount of money the player has
        """
        return self.wallet

    def set_wallet(self, wallet: int):
        """
        set_wallet is a method that sets the wallet of the player

        Parameters
        ----------
        wallet : int
            The amount of money the player has after the modification
        """
        self.wallet = wallet

    def get_name(self) -> str:
        """
        get_name is a method that returns the name of the player

        Returns
        -------
        str
            The name of the player
        """
        return self.name

    def get_games_played(self) -> int:
        """
        get_games_played is a method that returns the number of games the player has played

        Returns
        -------
        int
            The number of games the player has played
        """
        return self.games_played

    def get_games_won(self) -> int:
        """
        get_games_won is a method that returns the number of games the player has won

        Returns
        -------
        int
            The number of games the player has won
        """
        return self.games_won

    def get_nb_bankrupt(self) -> int:
        """
        get_nb_bankrupt is a method that returns the number of times the player has gone bankrupt (money = 0)

        Returns
        -------
        int
            The number of times the player has gone bankrupt
        """
        return self.nb_bankrupt

    def to_dict(self) -> dict:  # I added the type hint
        """
        to_dict is a method that returns a dictionary representation of the player

        Returns
        -------
        dict
            A dictionary containing the attributes of the player with the keys "name": str, "wallet": int, "games_played": int, "games_won": int, "nb_bankrupt": int
        """
        return {
            "name": self.name,
            "wallet": self.wallet,
            "games_played": self.games_played,
            "games_won": self.games_won,
            "nb_bankrupt": self.nb_bankrupt,
        }
