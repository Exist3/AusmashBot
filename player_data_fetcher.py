from discord.ext.commands import Bot
from discord import Game

BOT_PREFIX = "?"
TOKEN = "NTk3MDc0Njg0MjM5OTM3NTQ2.XSCzyA.sEfdg0OhySA88n4gD3L-KIw2gR4"

client = Bot(command_prefix=BOT_PREFIX,
             activity=Game(name="type " + BOT_PREFIX + "help for help"))


@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')



client.run(TOKEN)
