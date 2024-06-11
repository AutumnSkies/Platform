import discord
from discord.ext import commands
import random
import logging
import asyncio

token = 'token here'

description = '''Programmed by catgirlandamoth (Sadie)

Primary use case is rolling dice and helping with scheduling for sessions.

Prefix is p; - Sorry to pluralkit users ^^;'''

intents = discord.Intents.default()
intents.members = True
intents.message_content = True

bot = commands.Bot(command_prefix='p;', description=description, intents=intents)

# Configure Logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger('Platform')
handler = logging.FileHandler(filename='Platform.log', encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)

# Very advanced error handling

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, discord.ext.commands.errors.MissingRole) and "Role 'PlatformPermissions' is required to run this command" in str(error):
        await ctx.send("Every 60 seconds a minute passes in Ohio (Lacking PlatformPermissions role)")

@bot.event
async def on_ready():
    await bot.change_presence(activity=discord.Game(name="Are you sure you'd like to do that?"))
    print(f'Logged in as {bot.user} (ID: {bot.user.id})')
    print('------')

@bot.command()
async def roll(ctx, dice: str):
    """Rolls a dice in NdN format."""
    try:
        rolls, limit = map(int, dice.split('d'))
    except Exception:
        await ctx.send('ERROR:Syntax - Format has to be in NdN!')
        return

    result = ', '.join(str(random.randint(1, limit)) for r in range(rolls))
    await ctx.send(result)

@bot.command()
@commands.has_role("PlatformPermissions")
async def reaction(ctx):
    
    """Sets up reaction roles."""
    message = await ctx.send("React with 🐉 for DnD or 🤖 for Lancer")
    await message.add_reaction("🐉")
    await message.add_reaction("🤖")

@bot.event
async def on_reaction_add(reaction, user):
    if user.bot:
        return

    if reaction.message.content == "React with 🐉 for DnD or 🤖 for Lancer":
        if str(reaction.emoji) == "🐉":
            role = discord.utils.get(user.guild.roles, name="dnd")
            await user.add_roles(role)
        elif str(reaction.emoji) == "🤖":
            role = discord.utils.get(user.guild.roles, name="lancer")
            await user.add_roles(role)

bot.run(token, log_handler=handler)
