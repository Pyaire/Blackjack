import os
import discord
from src.classes.DAO import DAO
from src.classes.Table import Table
from src.classes.Player import Player
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("DISCORD_TOKEN")
BDD = DAO()
intents = discord.Intents.default()
intents.message_content = True
TABLE = None

client = discord.Client(intents=intents)


@client.event
async def on_ready():
    print(f"We have logged in as {client.user}")


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    elif message.content.startswith("$hello"):
        await message.channel.send(" Hello !")

    elif message.content.startswith("$profile"):
        author = str(message.author)
        profil_player: Player = BDD.find_by_name(author)
        if profil_player is None:
            await message.channel.send("You don't have a profile yet")
        else:
            profile = profil_player.to_dict()
            if profile["games_played"] == 0:
                pourcentage = "Na %"
            else:
                pourcentage = f"{profile['games_won'] / profile['games_played'] * 100} %"
            await message.channel.send(
                f"""
                        Name: {profile['name']}
            Wallet: {profile['wallet']} €
            Games played: {profile['games_played']}
            Games won: {profile['games_won']}
            Pourcentage of win: {pourcentage}
            Number of bankrupt: {profile['nb_bankrupt']}
            """
            )

    elif message.content.startswith("$create profile"):
        author = str(message.author.name)
        profil_player = BDD.find_by_name(author)
        if profil_player is not None:
            await message.channel.send("You already have a profile")
        else:
            BDD.insert(Player(author, 50, 0, 0, 0))
            await message.channel.send("Profile created, good luck !")

    elif message.content.startswith("$delete profile"):
        author = str(message.author.name)
        profil_player = BDD.find_by_name(author)
        if profil_player is None:
            await message.channel.send("You don't have a profile yet")
        else:
            BDD.delete(profil_player)
            await message.channel.send("Profile deleted")

    elif message.content.startswith("$refund") and str(message.author) == "aynost":
        player = str(message.mentions[0])
        profil_player = BDD.find_by_name(player)
        if profil_player is None:
            await message.channel.send(f"{player} don't have a profile yet")
        else:
            profil_player.set_wallet(message.content.split(" ")[2])
            BDD.update(profil_player)
            await message.channel.send("Refound done !")

    elif message.content.startswith("$close") or message.content.startswith("$cls") and str(message.author) == "aynost":
        global TABLE
        TABLE = None
        BDD.close()
        await message.channel.send("Bye ! ^^")
        await client.close()

    elif message.content.startswith("$create table"):
        author = str(message.author)
        profil_player = BDD.find_by_name(author)
        if profil_player is None:
            await message.channel.send("You don't have a profile yet")
        if TABLE is not None:
            await message.channel.send("You already have a table")
        else:
            TABLE = Table(profil_player, client)
            await message.channel.send("Table created, let's play !")

    elif message.content.startswith("$join table"):
        author = str(message.author)
        profil_player = BDD.find_by_name(author)
        if profil_player is None:
            await message.channel.send("You don't have a profile yet")
        if TABLE is None:
            await message.channel.send("You don't have a table yet")
        else:
            TABLE.add_player(profil_player)
            await message.channel.send("You joined the table")

    elif message.content.startswith("$leave table"):
        author = str(message.author)
        profil_player = BDD.find_by_name(author)
        if profil_player is None:
            await message.channel.send("You don't have a profile yet")
        if TABLE is None:
            await message.channel.send("You don't have a table yet")
        if TABLE.get_player(profil_player) is None:
            await message.channel.send("You are not in the table")
        else:
            TABLE.remove_player(profil_player)
            await message.channel.send("You left the table")

    elif message.content.startswith("$bet"):
        author = str(message.author)
        profil_player = BDD.find_by_name(author)
        if profil_player is None:
            await message.channel.send("You don't have a profile yet")
        if TABLE is None:
            await message.channel.send("You don't have a table yet")
        if TABLE.get_player(profil_player) is None:
            await message.channel.send("You are not in the table")
        else:
            if message.content.split(" ")[1].isnumeric() is False:
                await message.channel.send("You can't bet a string")
            elif int(message.content.split(" ")[1]) % 1 != 0:
                await message.channel.send("You can't bet a float")
            elif int(message.content.split(" ")[1]) > int(profil_player.wallet):
                await message.channel.send("You don't have enough money")
            elif int(message.content.split(" ")[1]) < 0:
                await message.channel.send("You can't bet a negative amount")
            elif int(message.content.split(" ")[1]) == 0:
                await message.channel.send("You can't bet 0")
            elif int(message.content.split(" ")[1]) % 5 != 0:
                await message.channel.send("You can't bet an amount that is not a multiple of 5")
            else:
                TABLE.bet(profil_player, int(message.content.split(" ")[1]))
                await message.channel.send("Bet done !")

    elif message.content.startswith("$see bet"):
        author = str(message.author)
        profil_player = BDD.find_by_name(author)
        if profil_player is None:
            await message.channel.send("You don't have a profile yet")
        if TABLE is None:
            await message.channel.send("You don't have a table yet")
        if TABLE.get_player(profil_player) is None:
            await message.channel.send("You are not in the table")
        else:
            await message.channel.send(f"Your bet: {TABLE.get_player(profil_player)['bet']} €")

    # elif message.content.startswith('$start'):
    #     author = str(message.author)
    #     profil_player = BDD.find_by_name(author)
    #     if profil_player is None:
    #         await message.channel.send("You don't have a profile yet")
    #     else:
    #         await message.channel.send("Let's play !")
    #         table = Table(profil_player, client)
    #         table.start_game()


client.run(TOKEN)
