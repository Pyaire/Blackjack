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
            "dealer": {"hand": [], "hand_stat": Hand_stat.IN},
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

    def stand(self, player_name: str):
        """
        stand is a method that makes a player stand

        Parameters
        ----------
        player_name : str
            The player that is standing
        """
        self.players[player_name]["hand_stat"] = Hand_stat.STAND

    def hit(self, player_name : str):
        """
        hit is a method that makes a player draw a card

        Parameters
        ----------
        player_name : str
            The player that is drawing a card
        """
        self.players[player_name]["hand"].append(self.deck.draw_card())
        self.players[player_name]["hand_stat"] = self.check_hand(player_name)

    def double(self, player_name : str):
        """
        double is a method that makes a player double his bet and draw a card

        Parameters
        ----------
        player_name : str
            The player that is doubling his bet and drawing a card
        """
        self.players[player_name]["bet"] *= 2
        self.players[player_name]["hand"].append(self.deck.draw_card())
        self.players[player_name]["hand_stat"] = self.check_hand(player_name)
        if(self.players[player_name]["hand_stat"] == Hand_stat.IN):
             self.players[player_name]["hand_stat"] = Hand_stat.STAND

    def split(self, player_name : str):
        """
        split is a method that makes a player split his hand

        Parameters
        ----------
        player_name : str
            The player that is splitting his hand
        """
        self.players[player_name + "-split"] = {
            "bet": self.players[player_name]["bet"],
            "hand": [self.players[player_name]["hand"].pop()],
            "insurance": False,
            "hand_stat": Hand_stat.IN,
            "to": player_name,
        }
        self.players[player_name]["hand"].append(self.deck.draw_card())
        self.players[player_name + "-split"]["hand"].append(self.deck.draw_card())

    def insurance(self, player_name : str):
        """
        insurance is a method that makes a player take insurance

        Parameters
        ----------
        player_name : Player
            The player that is taking insurance
        """
        self.players[player_name]["insurance"] = True

    def check_hand_value(self, player_name: str) -> Hand_stat:
        """
        check_hand is a method that checks the value of a player's hand

        Parameters
        ----------
        player_name : str
            The player whose hand is to be checked

        Returns
        -------
        Hand_value
            The value of the hand (From 0 to n)
        """
        hand_value = 0
        hand = self.players[player_name]["hand"]
        for card in hand:
            hand_value += card.value
        return hand_value

    def check_hand(self, player_name: str) -> Hand_stat:
        """
        check_hand is a method that checks the state of a player's hand

        Parameters
        ----------
        player_name : str
            The player whose hand is to be checked

        Returns
        -------
        Hand_stat
            The state of the hand (IN, BUST, BLACKJACK)
        """
        hand_value = 0
        hand = self.players[player_name]["hand"]
        for card in hand:
            hand_value += card.value
        if hand_value > 21:
            return Hand_stat.BUST
        if hand_value == 21 and len(self.players[player_name]["hand"]) == 2:
            return Hand_stat.BLACKJACK
        if hand_value == 21:
            return Hand_stat.STAND
        return Hand_stat.IN

    def check_blackjack(self, player_name : str) -> bool:
        """
        check_blackjack is a method that checks if a player has a blackjack

        Parameters
        ----------
        player_name : str
            The player whose hand is to be checked

        Returns
        -------
        bool
            True if the player has a blackjack, False otherwise
        """
        hand_value = 0
        hand = self.players[player_name]["hand"]
        for card in hand:
            hand_value += card.value
        if hand_value == 21:
            return True
        return False

    def bet(self, player_name : str, amount : int):
        """
        bet is a method that makes a player bet an a select amount of money

        Parameters
        ----------
        player_name : str
            The player that is betting
        amount : int
            The amount of money the player decided to bet
        """
        self.players[player_name]["bet"] = amount

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
        player_name = player.get_name()
        try:
            to_return = self.players[player_name]
        except:
            return None

    def get_player_hand(self, player_name : str) -> str:
        """
        get_player_hand is a method that returns player's hand as a string

        Parameters
        ----------
        player_name : str
            The player whose hand is to be returned

        Returns
        -------
        str
            List of cards (value & color)
        """
        player_hand = ""
        hand = self.players[player_name]["hand"]
        for card in hand:
            player_hand += card.to_print() + " "
        return player_hand
    
    async def play(self, player_name : str, channel : discord.Message.channel) :
        """
        play is a method that handles player's turn

        Parameters
        ----------
        player_name : str
            The player whose turn it is to play
        channel : discord.Message.channel
            The channel to post messages on
        """
        # TO-DO : handle insurance, handle split
        def check_decision(message):
            match message.content.capitalize():
                case "H" :
                    self.hit(player_name)
                case "S" :
                    self.stand(player_name)
                case "D" :
                    self.double(player_name)
                case _ :
                    return False
            return True
        while(self.players[player_name]["hand_stat"] == Hand_stat.IN):
            await channel.send(f"{player_name} : You have {self.get_player_hand(player_name)}")
            await channel.send("Do you want to hit [H], stand [S] or double[D] ?")
            await self.client.wait_for('message', check=check_decision)
            await channel.send(f"{player_name} state : {self.players[player_name]["hand_stat"]}, result {self.check_hand_value(player_name)}\n")
            print(f"{player_name} state : {self.players[player_name]["hand_stat"]}, result {self.check_hand_value(player_name)}\n")

    def check_win(self, player : Player) -> str:
        """
        check_win is a method that check player result and update wallet

        Parameters
        ----------
        player : Player
            The player whose hand is to be checked

        Returns
        -------
        str
            Result (Win / Loss / Draw / Blackjack)
        """
        if (self.players[player.get_name()]["hand_stat"] == Hand_stat.BLACKJACK and self.players["dealer"]["hand_stat"] != Hand_stat.BLACKJACK) :
            player.set_wallet(player.get_wallet() + 2.5 * self.players[player.get_name()]["bet"])
            return("Blackjack !")
        elif (self.players[player.get_name()]["hand_stat"] == Hand_stat.STAND and (self.check_hand_value("dealer") < self.check_hand_value(player.get_name()) or self.players["dealer"]["hand_stat"] == Hand_stat.BUST)) :
            player.set_wallet(player.get_wallet() + 2 * self.players[player.get_name()]["bet"])
            return("Win !")
        elif ((self.players[player.get_name()]["hand_stat"] == Hand_stat.BUST or self.check_hand_value("dealer") > self.check_hand_value(player.get_name())) and self.players["dealer"]["hand_stat"] != Hand_stat.BUST) :
            player.set_wallet(player.get_wallet() - self.players[player.get_name()]["bet"])
            return("Loss...")
        else :
            return("Push")
            
    # def start_game(self):
    #     for player in self.players:
    #         if player != 'dealer':
    #             self.players[player_name]['hand'] = self.deck.draw_card()
    #     self.players['dealer'] = self.deck.draw_card()
    #     for player in self.players:
    #         if player != 'dealer':
    #             self.players[player_name]['hand'] = self.deck.draw_card()
    #     for player in self.players:
    #         if self.check_blackjack(player):
    #             self.players[player_name]['hand_stat'] = Hand_stat.BLACKJACK
    #         while self.players[player_name]['hand_stat'] == Hand_stat.IN:
    #             ascii_hand = ''
    #             for card in self.players[player_name]['hand']:
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

    # def start_game():
    #     for player in self.players:
    #         if player != 'dealer':
    #             self.players[player_name]['hand'] = self.deck.draw_card()
    #     self.players['dealer'] = self.deck.draw_card()
    #     for player in self.players:
    #         if player != 'dealer':
    #             self.players[player_name]['hand'] = self.deck.draw_card()
    #     for player in self.players:
            # await message.channel.send(f"<@{player.id}> you're up !")


