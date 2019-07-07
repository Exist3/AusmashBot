from discord.ext.commands import Bot
from discord import Game
import os

BOT_PREFIX = "?"
TOKEN = os.environ.get("TOKEN")

client = Bot(command_prefix=BOT_PREFIX,
             activity=Game(name="type " + BOT_PREFIX + "help for help"))


@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')



client.run(TOKEN)
