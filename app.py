import os
import discord
from src.classes.DAO import DAO
from src.classes.Table import Table
from src.classes.Player import Player
from dotenv import load_dotenv

load_dotenv()

TOKEN=os.getenv('DISCORD_TOKEN')
BDD = DAO()
intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    elif message.content.startswith('$hello'):
        await message.channel.send(' Hello !')
    
    elif message.content.startswith('$profile'):
        author = str(message.author)
        profil_player: Player = BDD.find_by_name(author)
        if profil_player is None:
            await message.channel.send("You don't have a profile yet")
        else:
            profile = profil_player.to_dict()
            if profile['games_played'] == 0:
                pourcentage = 'Na %'
            else:
                pourcentage = f'{profile['games_won'] / profile['games_played'] * 100} %'
            await message.channel.send(f"""
                        Name: {profile['name']}
            Wallet: {profile['wallet']} 
            Games played: {profile['games_played']}
            Games won: {profile['games_won']}
            Pourcentage of win: {pourcentage}
            Number of bankrupt: {profile['nb_bankrupt']}
            """)


    elif message.content.startswith('$create profile'):
        author = str(message.author.name)
        profil_player = BDD.find_by_name(author)
        if profil_player is not None:
            await message.channel.send("You already have a profile")
        else:
            BDD.insert(Player(author, 50, 0, 0, 0))
            await message.channel.send("Profile created, good luck !")

    elif message.content.startswith('$delete profile'):
        author = str(message.author.name)
        profil_player = BDD.find_by_name(author)
        if profil_player is None:
            await message.channel.send("You don't have a profile yet")
        else:
            BDD.delete(profil_player)
            await message.channel.send("Profile deleted")

    elif message.content.startswith('$refund') and str(message.author) == 'aynost':
        player = str(message.mentions[0])
        profil_player = BDD.find_by_name(player)
        if profil_player is None:
            await message.channel.send(f"{player} don't have a profile yet")
        else:
            profil_player.set_wallet(message.content.split(' ')[2])
            BDD.update(profil_player)
            await message.channel.send("Refound done !")

    elif message.content.startswith('$close') or message.content.startswith('$cls') and str(message.author) == 'aynost':
        await message.channel.send('Bye ! ^^')
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
