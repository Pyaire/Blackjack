from src.classes.Player import Player
from src.classes.Deck import Deck
from src.enum.Hand_stat import Hand_stat

class Table:
    def __init__(self, player: Player, client):
        self.players = {'dealer':[], player:{'bet' : 0, 'hand': [], 'insurance' : False, 'hand_stat': Hand_stat.IN}}
        self.deck = Deck()
        self.deck.shuffle()
        self.client = client

    def add_player(self, player):
        self.player[str(player.name)] = {'bet' : 0, 'hand': [], 'insurance' : False, 'hand_stat': Hand_stat.IN}

    def remove_player(self, player):
        del self.player[str(player.name)]

    def stand(self, player):
        self.players[player]['hand_stat'] = Hand_stat.STAND

    def hit(self, player):
        self.players[player]['hand'].append(self.deck.draw_card())
        self.players[player]['hand_stat'] = self.check_hand(player)

    def double(self, player):
        self.players[player]['bet'] *= 2
        self.players[player]['hand'].append(self.deck.draw_card())
        self.players[player]['hand_stat'] = self.check_hand(player)

    def split(self, player):
        self.players[player+'-split'] = {'bet' : self.players[player]['bet'], 'hand': [self.players[player]['hand'].pop()], 'insurance' : False, 'hand_stat': Hand_stat.IN, 'to' : player}
        self.players[player]['hand'].append(self.deck.draw_card())
        self.players[player+'-split']['hand'].append(self.deck.draw_card())

    def insurance(self, player):
        self.players[player]['insurance'] = True

    def check_hand(self, player):
        hand_value = 0
        hand = self.players[player]['hand']
        for card in hand:
            hand_value += card.value
        if hand_value > 21:
            return Hand_stat.BUST
        if hand_value == 21:
            return Hand_stat.BLACKJACK
        return Hand_stat.IN

    def check_blackjack(self, player):
        hand_value = 0
        hand = self.players[player]['hand']
        for card in hand:
            hand_value += card.value
        if hand_value == 21:
            return True
        return False
    
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