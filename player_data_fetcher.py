from discord.ext.commands import Bot
from discord import Game
from dotenv import load_dotenv
import os
import api_requests as api

load_dotenv()
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
    except:
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
async def elo(ctx, player_name=None, player_region=None):
    if player_name is None or player_region is None:
        await ctx.send("Please ensure you use the following format: \n" +
                       BOT_PREFIX + "elo <player> <region>")
        return
    player = find_player(player_name, player_region)
    region = search_region(player_region)
    if player == -1:
        await ctx.send("Player not found.")
        return
    for result in player.get_elo():
        if result["Game"]["ID"] == GAME.id:
            await ctx.send("{} from {} has {} elo.".format(player.name, region.name, result["Elo"]))
            return
    await ctx.send("{} from {} has no recorded elo data for {}".format(player.name, region.name, GAME.name))


@client.command()
async def trueskill(ctx, player_name=None, player_region=None):
    if player_name is None or player_region is None:
        await ctx.send("Please ensure you use the following format: \n" +
                       BOT_PREFIX + "trueskill <player> <region>")
        return
    player = find_player(player_name, player_region)
    region = search_region(player_region)
    if player == -1:
        await ctx.send("Player not found.")
        return
    for result in player.get_trueskill():
        if result["Game"]["ID"] == GAME.id:
            await ctx.send("{} from {} has a mean trueskill of {}.".format(player.name, region.name, result["Mean"]))
            return
    await ctx.send("{} from {} has no recorded trueskill rating for {}".format(player.name, region.name, GAME.name))


@client.command()
async def stats(ctx, player_name_1=None, player_region_1=None, player_name_2=None, player_region_2=None):
    if player_name_1 is None or player_region_1 is None or player_name_2 is None or player_region_2 is None:
        await ctx.send("Please ensure you use the following format: \n" +
                       BOT_PREFIX + "stats <player> <region> <player2> <region2>")
        return
    player_1 = find_player(player_name_1, player_region_1)
    player_2 = find_player(player_name_2, player_region_2)
    if player_1 == -1 or player_2 == -1:
        await ctx.send("Player not found.")
        return
    stats = player_1.compare_stats(player_2, GAME)
    await ctx.send("{p1} and {p2} have played {matches} matches. \
    \n{p1} has won {p1wins} matches and {p2} has won {p2wins} matches. \
    \n{p1}'s win percentage is currently {winpercent}%".format
                   (p1=player_1.name, p2=player_2.name, matches=stats["Player1WinCount"] + stats["Player2WinCount"],
                    p1wins=stats["Player1WinCount"], p2wins=stats["Player2WinCount"],
                    winpercent=stats["Player1WinPercent"]))

client.run(TOKEN)
