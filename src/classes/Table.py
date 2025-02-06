import discord
from src.classes.Player import Player
from src.classes.Deck import Deck
from src.enum.Hand_stat import Hand_stat


class Table:
    """
    Table is a class that represents a blackjack table with a dealer and players
    """

    def __init__(self, player: Player, client: discord.Client):
        """
        __init__ is a method that initializes the Table object

        Parameters
        ----------
        player : Player
            The player that created the table and is going to play on it
        client : discord.Client
            The discord client that is going to be used to interact with the player
        """
        self.players = {
            "dealer": [],
            player.get_name(): {"bet": 0, "hand": [], "insurance": False, "hand_stat": Hand_stat.IN},
        }
        self.deck = Deck()
        self.deck.shuffle()
        self.client = client

    def add_player(self, player: Player):
        """
        add_player is a method that adds a player to the table

        Parameters
        ----------
        player : Player
            The player to add to the table
        """
        self.players[player.get_name()] = {"bet": 0, "hand": [], "insurance": False, "hand_stat": Hand_stat.IN}

    def remove_player(self, player: Player):
        """
        remove_player is a method that removes a player from the table

        Parameters
        ----------
        player : Player
            The player to remove from the table
        """
        del self.players[str(player.get_name())]

    def stand(self, player: Player):
        """
        stand is a method that makes a player stand

        Parameters
        ----------
        player : Player
            The player that is standing
        """
        player = player.get_name()
        self.players[player]["hand_stat"] = Hand_stat.STAND

    def hit(self, player : Player):
        """
        hit is a method that makes a player draw a card

        Parameters
        ----------
        player : Player
            The player that is drawing a card
        """
        player = player.get_name()
        self.players[player]["hand"].append(self.deck.draw_card())
        self.players[player]["hand_stat"] = self.check_hand(player)

    def double(self, player : Player):
        """
        double is a method that makes a player double his bet and draw a card

        Parameters
        ----------
        player : Player
            The player that is doubling his bet and drawing a card
        """
        player = player.get_name()
        self.players[player]["bet"] *= 2
        self.players[player]["hand"].append(self.deck.draw_card())
        self.players[player]["hand_stat"] = self.check_hand(player)

    def split(self, player : Player):
        """
        split is a method that makes a player split his hand

        Parameters
        ----------
        player : Player
            The player that is splitting his hand
        """
        player = player.get_name()
        self.players[player + "-split"] = {
            "bet": self.players[player]["bet"],
            "hand": [self.players[player]["hand"].pop()],
            "insurance": False,
            "hand_stat": Hand_stat.IN,
            "to": player,
        }
        self.players[player]["hand"].append(self.deck.draw_card())
        self.players[player + "-split"]["hand"].append(self.deck.draw_card())

    def insurance(self, player : Player):
        """
        insurance is a method that makes a player take insurance

        Parameters
        ----------
        player : Player
            The player that is taking insurance
        """
        player = player.get_name()
        self.players[player]["insurance"] = True

    def check_hand(self, player: Player) -> Hand_stat:
        """
        check_hand is a method that checks the value of a player's hand

        Parameters
        ----------
        player : Player
            The player whose hand is to be checked

        Returns
        -------
        Hand_stat
            The state of the hand (IN, BUST, BLACKJACK)
        """
        player = player.get_name()
        hand_value = 0
        hand = self.players[player]["hand"]
        for card in hand:
            hand_value += card.value
        if hand_value > 21:
            return Hand_stat.BUST
        if hand_value == 21:
            return Hand_stat.BLACKJACK
        return Hand_stat.IN

    def check_blackjack(self, player : Player) -> bool:
        """
        check_blackjack is a method that checks if a player has a blackjack

        Parameters
        ----------
        player : Player
            The player whose hand is to be checked

        Returns
        -------
        bool
            True if the player has a blackjack, False otherwise
        """
        player = player.get_name()
        hand_value = 0
        hand = self.players[player]["hand"]
        for card in hand:
            hand_value += card.value
        if hand_value == 21:
            return True
        return False

    def bet(self, player : Player, amount : int):
        """
        bet is a method that makes a player bet an a select amount of money

        Parameters
        ----------
        player : Player
            The player that is betting
        amount : int
            The amount of money the player decided to bet
        """
        player = player.get_name()
        self.players[player]["bet"] = amount

    def get_player(self, player : Player) -> dict:
        """
        get_player is a method that returns a player from the table to know if he is sit at it

        Parameters
        ----------
        player : Player
            The player to get from the table

        Returns
        -------
        dict
            The player from the table
        """
        player = player.get_name()
        try:
            to_return = self.players[player]
        except:
            return None

    # def start_game(self):
    #     for player in self.players:
    #         if player != 'dealer':
    #             self.players[player]['hand'] = self.deck.draw_card()
    #     self.players['dealer'] = self.deck.draw_card()
    #     for player in self.players:
    #         if player != 'dealer':
    #             self.players[player]['hand'] = self.deck.draw_card()
    #     for player in self.players:
    #         if self.check_blackjack(player):
    #             self.players[player]['hand_stat'] = Hand_stat.BLACKJACK
    #         while self.players[player]['hand_stat'] == Hand_stat.IN:
    #             ascii_hand = ''
    #             for card in self.players[player]['hand']:
    #                 ascii_hand += card.to_ascii()
    #             self.client.channel.send(f"""{player} hand: {ascii_hand}
    #             Dealer hand: {self.players['dealer'][0].to_ascii()}
    #             1. Hit :reapeat:
    #             2. Stand :octogonal_sign:
    #             3. Double :repeat_one:
    #             4. Split :left_right_arrow:
    #             5. Insurance :shield:
    #             """).add_reaction('🔁').add_reaction('🛑').add_reaction('🔂').add_reaction('↔️').add_reaction('🛡️')
    #             response = self.client.wait_for('reaction_add', check=lambda reaction, user: user == self.client.author and reaction.emoji in ['🔁', '🛑', '🔂', '↔️', '🛡️'])
    #             if response == '🔁':
    #                 self.hit(player)
    #             elif response == '🛑':
    #                 self.stand(player)
    #             elif response == '🔂':
    #                 self.double(player)
    #             elif response == '↔️':
    #                 self.split(player)
    #             elif response == '🛡️':
    #                 self.insurance(player)
