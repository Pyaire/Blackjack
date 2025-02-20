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
print(f"Added {player2.get_name()} to table !\n")

### TABLE.START

while(table.players[player1.get_name()]["bet"] == 0) :
    try:
        bet = int(input(f"{player1.get_name()} c'est votre tour de miser !"))
    except:
        continue
    else:
        table.bet(player1.get_name(), bet)
print(f"{player1.get_name()} has bet {table.players[player1.get_name()]["bet"]}\n")

while(table.players[player2.get_name()]["bet"] == 0) :
    try:
        bet = int(input(f"{player2.get_name()} c'est votre tour de miser !"))
    except:
        continue
    else:
        table.bet(player2.get_name(), bet)
print(f"{player2.get_name()} has bet {table.players[player2.get_name()]["bet"]}\n")

table.hit(player1.get_name())
print(f"{player1.get_name()} draws : {table.players[player1.get_name()]["hand"][0].to_print()}")
table.hit(player2.get_name())
print(f"{player2.get_name()} draws : {table.players[player2.get_name()]["hand"][0].to_print()}")

table.hit("dealer")
print(f"Dealer draws : {table.players["dealer"]["hand"][0].to_print()}\n")

table.hit(player1.get_name())
print(f"{player1.get_name()} draws : {table.players[player1.get_name()]["hand"][0].to_print()}")
table.hit(player2.get_name())
print(f"{player2.get_name()} draws : {table.players[player2.get_name()]["hand"][0].to_print()}")
print("\n")

table.play(player1.get_name())
table.play(player2.get_name())

table.hit("dealer")
hand_value = table.check_hand_value("dealer")
while hand_value < 17 :
    table.hit("dealer")
    hand_value = table.check_hand_value("dealer")
print(f"Dealer state : {table.players["dealer"]["hand_stat"]}, result : {hand_value}\n")

# Check Win/Loss
print(f"{player1.get_name()}")
print(table.check_win(player1))
print(f"state : {table.players[player1.get_name()]["hand_stat"]}, wallet : {player1.get_wallet()}")

# Check Win/Loss
print(f"{player2.get_name()}")
print(table.check_win(player2))
print(f"state : {table.players[player2.get_name()]["hand_stat"]}, wallet : {player2.get_wallet()}")
