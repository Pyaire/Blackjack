# %%
import os
from discord import Client, Intents
from src.classes.DAO import DAO
from src.classes.Table import Table
from src.classes.Player import Player
from src.enum.Hand_stat import Hand_stat
from dotenv import load_dotenv

load_dotenv()

DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")


class MyClient(Client):
    async def on_ready(self):
        print(f"Logged on as {self.user}!")

    async def on_message(self, message):
        if message.author == client.user : return
        print(f"Message from {message.author}: {message.content}")
        # await message.channel.send(f"<@{message.author.id}>: Oui")


intents = Intents.default()
intents.message_content = True

client = MyClient(intents=intents)
# client.run(DISCORD_TOKEN)

player1 = Player("player1", 0, 0, 0, 0)
player2 = Player("player2", 0, 0, 0, 0)
player1.set_wallet(100)
player2.set_wallet(100)

table = Table(player1, client)
print(f"Created table with {table.players} !")
table.add_player(player2)
print(f"Added {player2.get_name()} to table !")

### TABLE.START
table.bet(player1.get_name(), 10)
print(f"{player1.get_name()} has bet {table.players[player1.get_name()]["bet"]}")
table.bet(player2.get_name(), 20)
print(f"{player2.get_name()} has bet {table.players[player2.get_name()]["bet"]}")
table.hit("dealer")
print(f"Dealer draws : {table.players["dealer"]["hand"][0].to_print()}")

table.hit(player1.get_name())
print(f"{player1.get_name()} draws : {table.players[player1.get_name()]["hand"][0].to_print()}")
table.hit(player2.get_name())
print(f"{player2.get_name()} draws : {table.players[player2.get_name()]["hand"][0].to_print()}")

table.hit(player1.get_name())
table.hit(player1.get_name())
print(f"{player1.get_name()} state : {table.players[player1.get_name()]["hand_stat"]}")
player1_hand = ""
hand = table.players[player1.get_name()]["hand"]
for card in hand:
    player1_hand += card.to_print() + " "
if (table.players[player1.get_name()]["hand_stat"] != Hand_stat.BLACKJACK and table.players[player1.get_name()]["hand_stat"] != Hand_stat.BUST) :
    table.stand(player1.get_name())
print(f"{player1.get_name()} state : {table.players[player1.get_name()]["hand_stat"]}, content : {player1_hand}, result {table.check_hand_value(player1.get_name())}")

table.hit(player2.get_name())
table.hit(player2.get_name())
player2_hand = ""
hand = table.players[player2.get_name()]["hand"]
for card in hand:
    player2_hand += card.to_print() + "  "

if (table.players[player2.get_name()]["hand_stat"] != Hand_stat.BLACKJACK and table.players[player2.get_name()]["hand_stat"] != Hand_stat.BUST) :
    table.stand(player2.get_name())
print(f"{player2.get_name()} state : {table.players[player2.get_name()]["hand_stat"]}, content : {player2_hand}, result {table.check_hand_value(player2.get_name())}")

table.hit("dealer")
hand_value = table.check_hand_value("dealer")
while hand_value < 17 :
    table.hit("dealer")
    hand_value = table.check_hand_value("dealer")
print(f"Dealer state : {table.players["dealer"]["hand_stat"]}, result : {hand_value}")

# Check Win/Loss
if (table.players[player1.get_name()]["hand_stat"] == Hand_stat.BLACKJACK and table.players["dealer"]["hand_stat"] != Hand_stat.BLACKJACK) :
    player1.set_wallet(player1.get_wallet() + 2.5 * table.players[player1.get_name()]["bet"])
    print("Blackjack !")
elif (table.players[player1.get_name()]["hand_stat"] == Hand_stat.STAND and (table.check_hand_value("dealer") < table.check_hand_value(player1.get_name()) or table.players["dealer"]["hand_stat"] == Hand_stat.BUST)) :
    player1.set_wallet(player1.get_wallet() + 2 * table.players[player1.get_name()]["bet"])
    print("Win !")
elif ((table.players[player1.get_name()]["hand_stat"] == Hand_stat.BUST or table.check_hand_value("dealer") > table.check_hand_value(player1.get_name())) and table.players["dealer"]["hand_stat"] != Hand_stat.BUST) :
    player1.set_wallet(player1.get_wallet() - table.players[player1.get_name()]["bet"])
    print("Loss...")
print(f"{player1.get_name()} state : {table.players[player1.get_name()]["hand_stat"]}, wallet : {player1.get_wallet()}")

# Check Win/Loss
if (table.players[player2.get_name()]["hand_stat"] == Hand_stat.BLACKJACK and table.players["dealer"]["hand_stat"] != Hand_stat.BLACKJACK) :
    player2.set_wallet(player2.get_wallet() + 2.5 * table.players[player2.get_name()]["bet"])
    print("Blackjack !")
elif (table.players[player2.get_name()]["hand_stat"] == Hand_stat.STAND and (table.check_hand_value("dealer") < table.check_hand_value(player2.get_name()) or table.players["dealer"]["hand_stat"] == Hand_stat.BUST)) :
    player2.set_wallet(player2.get_wallet() + 2 * table.players[player2.get_name()]["bet"])
    print("Win !")
elif ((table.players[player2.get_name()]["hand_stat"] == Hand_stat.BUST or table.check_hand_value("dealer") > table.check_hand_value(player2.get_name())) and table.players["dealer"]["hand_stat"] != Hand_stat.BUST) :
    player2.set_wallet(player2.get_wallet() - table.players[player2.get_name()]["bet"])
    print("Loss...")

print(f"{player2.get_name()} state : {table.players[player2.get_name()]["hand_stat"]}, wallet : {player2.get_wallet()}")
