from typing import Optional
import discord
from discord.ext import commands, tasks
from discord.ext.commands.core import check
from discord_together import DiscordTogether
from decouple import config
from discord_components import DiscordComponents, Button

intents = discord.Intents.default()
intents.members = True
intents.presences = True
intents.messages = True


cross = "<:red_cross:917650316512620544>"
tick = "<:green_tick:917650630405926912>"

#kana variables
token = config("TOKEN")
kana_id = 857835279259664403
client = commands.Bot(command_prefix=commands.when_mentioned_or(','), case_insensitive=True, intents=intents)
client.remove_command("help")

DT_OPTIONS = {
    "yt" : "youtube",
    "ytd": "880218832743055411",
    "sa" : "879864070101172255",
    "pp" : "763133495793942528",
    "dc" : "doodle-crew",
    "pr" : "poker",
    "bt" : "betrayal",
    "fh" : "fishing",
    "cs" : "chess",
    "lt" : "letter-tile",
    "ws" : "word-snack",
    "sc" : "spellcast",
    "aw" : "awkword",
    "ck" : "checkers"
}

DT_NAMES = {
    "yt" : "YouTube",
    "ytd": "YouTube Dev",
    "sa" : "Sketchy Artist",
    "pp" : "PuttyParty",
    "dc" : "Doodle Crew",
    "pr" : "Poker Night",
    "bt" : "Betrayal.io",
    "fh" : "Fishington.io",
    "cs" : "Chess",
    "lt" : "Letter Tile",
    "ws" : "Word Snack",
    "sc" : "SpellCast",
    "aw" : "AwkWord",
    "ck" : "Checkers"
}

print(">> DT is awaking...")

def check_event(event):
    for option in list(DT_OPTIONS.keys()):
        if option == event:
            return True
    return False

def get_btn(arg, link=None):
    h_components = [
        [
            Button(style=5, label="Invite Me", url="https://discord.com/api/oauth2/authorize?client_id=917640198689546312&permissions=137492811072&scope=bot%20applications.commands", emoji=discord.PartialEmoji(name="invite", id="918000296775520318")),
            Button(style=1, label="Games List", emoji=discord.PartialEmoji(name="list", id="918000306128814130")),
            Button(style=5, label="Support Server", url="https://discord.gg/7CYP8pKzDB", emoji=discord.PartialEmoji(name="support", id="918006066388795392"))
        ],
    ]
    g_components = [
        [
            Button(style=5, label="Invite Me", url="https://discord.com/api/oauth2/authorize?client_id=917640198689546312&permissions=137492811072&scope=bot%20applications.commands", emoji=discord.PartialEmoji(name="invite", id="918000296775520318")),
            Button(style=5, label="Support Server", url="https://discord.gg/7CYP8pKzDB", emoji=discord.PartialEmoji(name="support", id="918006066388795392")) 
        ],
    ]
    s_components = [
        [
            Button(style=5, label="Start Game", url=link, emoji=discord.PartialEmoji(name="blue_tick", id="918000693531508757")),
            Button(style=5, label="Invite Me", url="https://discord.com/api/oauth2/authorize?client_id=917640198689546312&permissions=137492811072&scope=bot%20applications.commands", emoji=discord.PartialEmoji(name="invite", id="918000296775520318")),
            Button(style=5, label="Support Server", url="https://discord.gg/7CYP8pKzDB", emoji=discord.PartialEmoji(name="support", id="918006066388795392")) 
        ],
    ]
    if arg == "h":
        return h_components
    elif arg == "g":
        return g_components
    elif arg == "s":
        return s_components

def get_embed(game, user):
    embed = discord.Embed(
        description=f"{tick} Game created ~ `{DT_NAMES[game]}`\n*Please click on the `Start Game` button below to start the game so that others can join you.*",
        color=0xffb0cd
    )
    embed.set_author(
        name=f"Join {user.name} for {DT_NAMES[game]}!",
        icon_url = user.avatar_url
    )
    return embed

@client.event
async def on_ready():
    await client.change_presence(status=discord.Status.online, activity=discord.Activity(type=discord.ActivityType.playing, name=f"Discord Together!"))
    client.togetherControl = await DiscordTogether(token)
    DiscordComponents(client)
    print("DT online")

@client.command()
async def games(ctx):
    desc = "> `1. ` ~ `YouTube Together      ` ~ `yt`\n> `2. ` ~ `YouTube Together (Dev)` ~ `ytd`\n> `3. ` ~ `Sketchy Artist        ` ~ `sa`\n> `4. ` ~ `Putt Party            ` ~ `pp`\n> `5. ` ~ `Doodle Crew           ` ~ `dc`\n> `6. ` ~ `Poker Night           ` ~ `pr`\n> `7. ` ~ `Betrayal.io           ` ~ `bt`\n> `8. ` ~ `Fishington.io         ` ~ `fh`\n> `9. ` ~ `Chess                 ` ~ `cs`\n> `10.` ~ `Letter Tile           ` ~ `lt`\n> `11.` ~ `Word Snack             ` ~ `ws`\n> `12.` ~ `Spell Cast            ` ~ `sc`\n> `13.` ~ `AwkWord               ` ~ `aw`\n> `14.` ~ `Checkers              ` ~ `ck`\n"
    emb = discord.Embed(
        description=desc,
        colour=0xffb0cd
    )
    emb.set_author(
        name="Game List",
        icon_url=ctx.author.avatar_url
    )
    emb.set_footer(
        text="Send ,start [prefix for game] to start a game"
    )
    await ctx.send(embed=emb, components=get_btn("g"))

@client.command()
async def help(ctx):
    embed = discord.Embed(
        description="*Developed by ~ [`asheeshh#7727`](https://discordapp.com/users/784363251940458516) using [`discord-together`](https://github.com/apurv-r/discord-together)*\n\nDiscord Together Bot allows you to access Games which are yet in Beta and play them with your friends!\n*Usage: `,start game_prefix` to start the game.*\n\n*Use `,games` to see the list of games available and their prefixes.*",
        colour=0xffb0cd
    )
    embed.set_author(
        name="Need Help?",
        icon_url=ctx.author.avatar_url
    )
    await ctx.send(embed=embed, components=get_btn("h"))

@client.command()
async def start(ctx, *, option=None):
    if ctx.author.voice is None:
        embed = discord.Embed(description=f"{cross} Please join a `Voice channel` to start a game!", colour=0xffb0cd)
        await ctx.send(embed=embed)
    else:
        if option is None:
            embed = discord.Embed(description=f"{cross} Please provide a game prefix to start a game! You can see the available games and their prefixes using `,games` command.", colour=0xffb0cd)
            await ctx.send(embed=embed)
        if option is not None and check_event(option):
            link = await client.togetherControl.create_link(ctx.author.voice.channel.id, f'{DT_OPTIONS[option]}')
            emb = get_embed(option, ctx.author)
            await ctx.send(f"Click on the `Start Game` button below to get started!", embed=emb, components=get_btn("s", link))
        elif option is not None and not check_event(option):
            embed = discord.Embed(description=f"{cross} No game found! Please send `,games` to check all the games available.", colour=0xffb0cd)
            await ctx.send(embed = embed)

@client.event
async def on_button_click(interaction):
    desc = "> `1. ` ~ `YouTube Together` ~ `yt`\n> `2. ` ~ `Doodle Crew` ~ `dc`\n> `3. ` ~ `Poker` ~ `pr`\n> `4. ` ~ `Betrayal.io` ~ `bt`\n> `5. ` ~ `Fishington.io` ~ `fh`\n> `6. ` ~ `Chess` ~ `cs`\n> `7. ` ~ `Letter Tile` ~ `lt`\n> `8. ` ~ `Word Snack` ~ `ws`\n> `9. ` ~ `Spell Cast` ~ `sc`\n> `10.` ~ `AwkWord` ~ `aw`\n> `11.` ~ `Checkers` ~ `ck`\n"
    emb = discord.Embed(
        description=desc,
        colour=0xffb0cd
    )
    emb.set_author(
        name="Game List",
        icon_url=interaction.user.avatar_url
    )
    emb.set_footer(
        text="Send ,start [prefix for game] to start a game"
    )
    if interaction.component.label.lower() == "games list":
        await interaction.respond(type=4, embed=emb)

client.run(token)
