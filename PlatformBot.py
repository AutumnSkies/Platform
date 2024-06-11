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


@bot.event
async def on_ready():
   await bot.change_presence(activity=discord.Game(name="Are you sure you'd like to do that?"))

@bot.event
async def on_ready():
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




bot.run(token, log_handler=handler)
