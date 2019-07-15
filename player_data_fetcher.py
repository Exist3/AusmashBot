from discord.ext.commands import Bot
from discord import Game
import os
import api_requests as api

BOT_PREFIX = "?"
TOKEN = os.environ.get("TOKEN")

GAME = api.Game(13)

REGIONS = []
for region in api.Region.get_regions():
    REGIONS.append(api.Region(region['ID']))

def search_region(term):
    for region in REGIONS:
        if region.name.upper() == term.upper() or region.short == term.upper():
            return region
    return None

def find_player(name, region):
    try:
        return api.Player(api.Player.get_player(name=name, region=search_region(region))["ID"])
    except api.IncorrectArgumentsError:
        return -1

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
    player = find_player(player_name, player_region)
    if player == -1:
        await ctx.send("Please use a valid region.")
        return
    for result in player.get_elo():
        if result["Game"]["ID"] == GAME.id:
            await ctx.send("{} from {} has {} elo.".format(player_name, player_region, result["Elo"]))
            return
    await ctx.send("{} from {} has no recorded elo data for {}".format(player_name, player_region, GAME.name))


@client.command()
async def trueskill(ctx, player_name, player_region):
    player = find_player(player_name, player_region)
    if player == -1:
        await ctx.send("Please use a valid region.")
        return
    for result in player.get_trueskill():
        if result["Game"]["ID"] == GAME.id:
            await ctx.send("{} from {} has a mean trueskill of {}.".format(player_name, player_region.name, result["Mean"]))
            return
    await ctx.send("{} from {} has no recorded trueskill rating for {}".format(player_name, player_region.name, GAME.name))
client.run(TOKEN)

#@client.command()
#async def
