import os
import discord
import src.controler as controler
from src.classes.DAO import DAO
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
        controler.send_hello(message=message)

    elif message.content.startswith("$profile"):
        controler.see_profil(message=message, DAO=BDD)

    elif message.content.startswith("$create profile"):
        controler.create_profil(message=message, DAO=BDD)

    elif message.content.startswith("$delete profile"):
        controler.delete_profil(message=message, DAO=BDD)

    elif message.content.startswith("$refund") and str(message.author) == "aynost":
        controler.refund(message=message, DAO=BDD)

    elif message.content.startswith("$create table"):
        controler.create_table(message=message, DAO=BDD)

    elif message.content.startswith("$join table"):
        controler.join_table(message=message, DAO=BDD)

    elif message.content.startswith("$leave table"):
        controler.leave_table(message=message, DAO=BDD)

    elif message.content.startswith("$bet"):
        controler.make_bet(message=message, DAO=BDD)

    elif message.content.startswith("$see bet"):
        controler.see_bet(message=message, DAO=BDD)

    elif message.content.startswith("$close") or message.content.startswith("$cls") and str(message.author) == "aynost":
        global TABLE
        TABLE = None
        BDD.close()
        await message.channel.send("Bye ! ^^")
        await client.close()
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
