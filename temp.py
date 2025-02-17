# %%
import os
from discord import Client, Intents
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
client.run(DISCORD_TOKEN)
