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

game = False
class MyClient(Client):
    async def on_ready(self):
        print(f"Logged on as {self.user}!")

    async def on_message(self, message):
        if message.author == client.user : return
        if message.content.startswith("$stop"):
            game = False
        if message.content.startswith("$start game"):
            game = True
            player1 = Player("player1", 0, 0, 0, 0)
            player2 = Player("player2", 0, 0, 0, 0)
            player1.set_wallet(100)
            player2.set_wallet(100)

            table = Table(player1, client)
            print(f"Created table with {table.players} !")
            await message.channel.send(f"Created table with {table.players} !")
            table.add_player(player2)
            print(f"Added {player2.get_name()} to table !\n")
            await message.channel.send(f"Added {player2.get_name()} to table !")

            ### TABLE.START
            while(game):
                print(game)
                def check(message):
                    try:
                        bet = int(message.content)
                    except:
                        return False
                    else:
                        return int(message.content)
                
                await message.channel.send(f"{player1.get_name()} c'est votre tour de miser !")
                bet_message = await self.wait_for('message', check=check)
                table.bet(player1.get_name(), int(bet_message.content))
                await message.channel.send(f"{player1.get_name()} has bet {table.players[player1.get_name()]["bet"]}")
                
                await message.channel.send(f"{player2.get_name()} c'est votre tour de miser !")
                bet_message = await self.wait_for('message', check=check)
                table.bet(player2.get_name(), int(bet_message.content))
                await message.channel.send(f"{player2.get_name()} has bet {table.players[player2.get_name()]["bet"]}")
                
                # while(table.players[player2.get_name()]["bet"] == 0) :
                #     try:
                #         bet = int(input(f"{player2.get_name()} c'est votre tour de miser !"))
                #     except:
                #         continue
                #     else:
                #         table.bet(player2.get_name(), bet)
                # print(f"{player2.get_name()} has bet {table.players[player2.get_name()]["bet"]}\n")
                # await message.channel.send(f"{player2.get_name()} has bet {table.players[player2.get_name()]["bet"]}\n")

                table.hit(player1.get_name())
                print(f"{player1.get_name()} draws : {table.players[player1.get_name()]["hand"][0].to_print()}")
                await message.channel.send(f"{player1.get_name()} draws : {table.players[player1.get_name()]["hand"][0].to_print()}")
                table.hit(player2.get_name())
                print(f"{player2.get_name()} draws : {table.players[player2.get_name()]["hand"][0].to_print()}")
                await message.channel.send(f"{player2.get_name()} draws : {table.players[player2.get_name()]["hand"][0].to_print()}")

                table.hit("dealer")
                print(f"Dealer draws : {table.players["dealer"]["hand"][0].to_print()}\n")
                await message.channel.send(f"Dealer draws : {table.players["dealer"]["hand"][0].to_print()}\n")

                table.hit(player1.get_name())
                print(f"{player1.get_name()} draws : {table.players[player1.get_name()]["hand"][0].to_print()}")
                await message.channel.send(f"{player1.get_name()} draws : {table.players[player1.get_name()]["hand"][0].to_print()}")
                table.hit(player2.get_name())
                print(f"{player2.get_name()} draws : {table.players[player2.get_name()]["hand"][0].to_print()}")
                await message.channel.send(f"{player2.get_name()} draws : {table.players[player2.get_name()]["hand"][0].to_print()}")
                print("\n")

                await table.play(player1.get_name(), message.channel)
                await table.play(player2.get_name(), message.channel)

                table.hit("dealer")
                hand_value = table.check_hand_value("dealer")
                while hand_value < 17 :
                    table.hit("dealer")
                    hand_value = table.check_hand_value("dealer")
                print(f"Dealer state : {table.players["dealer"]["hand_stat"]}, result : {hand_value}\n")
                await message.channel.send(f"Dealer state : {table.players["dealer"]["hand_stat"]}, result : {hand_value}\n")

                # Check Win/Loss
                print(f"{player1.get_name()}")
                print(table.check_win(player1))
                print(f"state : {table.players[player1.get_name()]["hand_stat"]}, wallet : {player1.get_wallet()}")

                await message.channel.send(f"**{player1.get_name()}** : {table.check_win(player1)}, wallet : {player1.get_wallet()}")

                # Check Win/Loss
                print(f"{player2.get_name()}")
                print(table.check_win(player2))
                print(f"state : {table.players[player2.get_name()]["hand_stat"]}, wallet : {player2.get_wallet()}")

                await message.channel.send(f"**{player2.get_name()}** : {table.check_win(player2)}, wallet : {player2.get_wallet()}")

                # Prepare new turn
                cards_drawn = []
                for i in table.players[player1.get_name()]["hand"]:
                    cards_drawn.append(table.players[player1.get_name()]["hand"].pop())

                for i in table.players[player2.get_name()]["hand"]:
                    cards_drawn.append(table.players[player2.get_name()]["hand"].pop())

                # for i in cards_drawn:
                #     table.deck.append(cards_drawn.pop())
                table.deck.build()
                table.deck.shuffle()

                await message.channel.send("Fin du tour, continue ? Y/N")
                def check_continue(message):
                    match message.content.capitalize():
                        case "Y" :
                            return True
                        case "N" :
                            game = False
                            return True
                        case _ :
                            return False
                await self.wait_for('message', check=check_continue)
intents = Intents.default()
intents.message_content = True

client = MyClient(intents=intents)
client.run(DISCORD_TOKEN)
