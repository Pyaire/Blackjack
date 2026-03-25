import os
from typing import Optional

import discord
from dotenv import load_dotenv

from src.classes.Player import Player
from src.classes.DAO import DAO
from src.classes.Table import Table

load_dotenv()

TOKEN = os.getenv("DISCORD_TOKEN")
intents = discord.Intents.default()
intents.message_content = True
TABLE: Optional[Table] = None

client = discord.Client(intents=intents)

async def send_hello(message: discord.Message) -> None:
    """Send a simple greeting message in the same channel.

    Parameters
    ----------
    message : discord.Message
        The Discord message context that triggered the command.

    Returns
    -------
    None
    """
    await message.channel.send(" Hello !")

async def see_profil(message: discord.Message, DAO: DAO) -> None:
    """Retrieve and display the profile of the message author.

    Parameters
    ----------
    message : discord.Message
        The Discord message context with author identity.
    DAO : DAO
        Data access object implementing find_by_name(name) and record retrieval.

    Returns
    -------
    None
    """
    author = str(message.author)
    profil_player: Optional[Player] = DAO.find_by_name(author)
    if profil_player is None:
        await create_profil(message=message, DAO=DAO)
    await message.channel.send(embed=profil_player.display_player())

async def create_profil(message: discord.Message, DAO: DAO) -> None:
    """Create a player profile for the author if it doesn't exist.

    Parameters
    ----------
    message : discord.Message
        The Discord message context with author identity.
    DAO : DAO
        Data access object implementing find_by_name(name) and insert(player).

    Returns
    -------
    None
    """
    author = str(message.author.name)
    profil_player: Optional[Player] = DAO.find_by_name(author)
    if profil_player is not None:
        await message.channel.send("You already have a profile")
    else:
        DAO.insert(Player(author, 50, 0, 0, 0))
        await message.channel.send("Profile created, good luck !")

async def delete_profil(message: discord.Message, DAO: DAO) -> None:
    """Delete the profile of the message author if it exists.

    Parameters
    ----------
    message : discord.Message
        The Discord message context with author identity.
    DAO : DAO
        Data access object implementing find_by_name(name) and delete(player).

    Returns
    -------
    None
    """
    author = str(message.author.name)
    profil_player: Optional[Player] = DAO.find_by_name(author)
    if profil_player is None:
        await message.channel.send("You don't have a profile yet")
    else:
        DAO.delete(profil_player)
        await message.channel.send("Profile deleted")

async def refund(message: discord.Message, DAO: DAO) -> None:
    """Refund a specific user mentioned in the message.

    Parameters
    ----------
    message : discord.Message
        The Discord message context with mention and content.
    DAO : DAO
        Data access object implementing find_by_name(name) and update(player).

    Returns
    -------
    None
    """
    player = str(message.mentions[0])
    profil_player: Optional[Player] = DAO.find_by_name(player)
    if profil_player is None:
        await message.channel.send(f"{player} don't have a profile yet")
    else:
        profil_player.set_wallet(int(message.content.split(" ")[2]))
        DAO.update(profil_player)
        await message.channel.send("Refound done !")

async def create_table(message: discord.Message, DAO: DAO) -> None:
    """Create a new table for the author (and profile if needed).

    Parameters
    ----------
    message : discord.Message
        The Discord message context with author identity.
    DAO : DAO
        Data access object implementing find_by_name(name) and insert(player).

    Returns
    -------
    None
    """
    global TABLE

    author = str(message.author)
    profil_player: Optional[Player] = DAO.find_by_name(author)
    if profil_player is None:
        DAO.insert(Player(author, 50, 0, 0, 0))
        await message.channel.send("Your profil and the table has been created")
        profil_player = DAO.find_by_name(author)

    if TABLE is not None:
        await message.channel.send("You already have a table")
    else:
        assert profil_player is not None
        TABLE = Table(profil_player, client)
        await message.channel.send("Table created, let's play !")

async def join_table(message: discord.Message, DAO: DAO) -> None:
    """Join an existing table or create if none exists.

    Parameters
    ----------
    message : discord.Message
        The Discord message context with author identity.
    DAO : DAO
        Data access object implementing find_by_name(name) and insert(player).

    Returns
    -------
    None
    """
    global TABLE

    author = str(message.author)
    profil_player: Optional[Player] = DAO.find_by_name(author)
    if profil_player is None:
        DAO.insert(Player(author, 50, 0, 0, 0))
        await message.channel.send("Your profil has been created")
        profil_player = DAO.find_by_name(author)

    assert profil_player is not None
    if TABLE is None:
        TABLE = Table(profil_player, client)
        await message.channel.send("You created and joined the table")
    else:
        TABLE.add_player(profil_player)
        await message.channel.send("You joined the table")

async def leave_table(message: discord.Message, DAO: DAO) -> None:
    """Leave the table if the author is currently seated.

    Parameters
    ----------
    message : discord.Message
        The Discord message context with author identity.
    DAO : DAO
        Data access object implementing find_by_name(name) and insert(player).

    Returns
    -------
    None
    """
    global TABLE

    author = str(message.author)
    profil_player: Optional[Player] = DAO.find_by_name(author)
    if profil_player is None:
        DAO.insert(Player(author, 50, 0, 0, 0))
        await message.channel.send("Your profil has been created, join a table to bet something")
        profil_player = DAO.find_by_name(author)

    if TABLE is None:
        await message.channel.send("You don't have a table yet")
        return

    assert profil_player is not None
    if TABLE.get_player(profil_player) is None:
        await message.channel.send("You are not in the table")
    else:
        TABLE.remove_player(profil_player)
        await message.channel.send("You left the table")

async def make_bet(message: discord.Message, DAO: DAO) -> None:
    """Place a bet for the author's player if allowed.

    Parameters
    ----------
    message : discord.Message
        The Discord message context with author identity and bet command arguments.
    DAO : DAO
        Data access object implementing find_by_name(name) and insert(player).

    Returns
    -------
    None
    """
    author = str(message.author)
    profil_player: Optional[Player] = DAO.find_by_name(author)
    if profil_player is None:
        DAO.insert(Player(author, 50, 0, 0, 0))
        await message.channel.send("Your profil has been created, join a table to bet something")
        return

    if TABLE is None:
        await message.channel.send("You don't have a table yet")
        return

    assert profil_player is not None
    if TABLE.get_player(profil_player) is None:
        await message.channel.send("You are not in the table")
        return

    amount_to_bet = message.content.split(" ")[1]
    if not amount_to_bet.isnumeric():
        await message.channel.send("You can't bet a string")
    elif int(amount_to_bet) % 1 != 0:
        await message.channel.send("You can't bet a float")
    elif int(amount_to_bet) > int(profil_player.wallet):
        await message.channel.send("You don't have enough money")
    elif int(amount_to_bet) < 0:
        await message.channel.send("You can't bet a negative amount")
    elif int(amount_to_bet) == 0:
        await message.channel.send("You can't bet 0")
    elif int(amount_to_bet) % 5 != 0:
        await message.channel.send("You can't bet an amount that is not a multiple of 5")
    else:
        TABLE.bet(profil_player, int(amount_to_bet))
        await message.channel.send("Bet done !")

async def see_bet(message: discord.Message, DAO: DAO) -> None:
    """Show the author’s current bet on the table.

    Parameters
    ----------
    message : discord.Message
        The Discord message context with author identity.
    DAO : DAO
        Data access object implementing find_by_name(name) and insert(player).

    Returns
    -------
    None
    """
    author = str(message.author)
    profil_player: Optional[Player] = DAO.find_by_name(author)
    if profil_player is None:
        DAO.insert(Player(author, 50, 0, 0, 0))
        await message.channel.send("Your profil has been created, join a table to bet something")
        return

    if TABLE is None:
        await message.channel.send("You don't have a table yet")
        return

    assert profil_player is not None
    if TABLE.get_player(profil_player) is None:
        await message.channel.send("You are not in the table")
    else:
        await message.channel.send(f"Your bet: {TABLE.get_player(profil_player)['bet']} €")