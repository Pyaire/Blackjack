class Player:
    def __init__(self, name: str, wallet: int, games_played: int, games_won: int, nb_bankrupt: int):
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


    def get_wallet(self):
        return self.wallet

    def get_name(self):
        return self.name
    
    def get_games_played(self):
        return self.games_played
    
    def get_games_won(self):
        return self.games_won
    
    def get_nb_bankrupt(self):
        return self.nb_bankrupt
    
    def to_dict(self):
        return {"name": self.name, "wallet": self.wallet, "games_played": self.games_played, "games_won": self.games_won, "nb_bankrupt": self.nb_bankrupt}