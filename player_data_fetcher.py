from discord.ext.commands import Bot
from discord import Game
import os
import api_requests as api

BOT_PREFIX = "?"
TOKEN = os.environ.get("TOKEN")

game = api.Game(13)


client = Bot(command_prefix=BOT_PREFIX,
             activity=Game(name="type " + BOT_PREFIX + "help for help"))


@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')


@client.command()
async def elo(ctx, player_name, player_region):
    print(player_name)
    print(player_region)
    player = api.Player(api.Player.get_player(name=player_name, region=player_region)["ID"])
    for result in player.get_elo():
        if result["Game"]["ID"] == game.id:
            await ctx.send("{} from {} has {} elo.".format(player_name, player_region, result["Elo"]))
            return
    await ctx.send("{} from {} has no recorded data for {}".format(player_name, player_region, game.name))

client.run(TOKEN)
