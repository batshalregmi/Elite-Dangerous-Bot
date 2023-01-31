import asyncio
import os
import aiohttp
import discord
import random
import cogs


from datetime import datetime
from discord.ext import commands
from dotenv import load_dotenv
from cprint import cprint as logging


load_dotenv()
intents = discord.Intents.default()

bot = commands.Bot(
    command_prefix=commands.when_mentioned_or(os.getenv("PREFIX")),
    case_insensitive=True,
    description="A bot for tracking stats in Elite Dangerous.",
    intents=intents,
)
bot.load_extension("cogs.SystemStats")

bot.log = logging

try:
    import uvloop
except ImportError:
    bot.log.err(
        "Failed to import uvloop. Make sure you have installed it. (It might not be supported on windows)",
        False,
    )
else:
    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())
    bot.log.info("Using uvloop")


@bot.event
async def on_ready():
    bot.log.info("{} is ready".format(bot.user))
    now = datetime.utcnow().time().strftime("%H:%M:%S")
    bot.log.info("Current UTC time: {}".format(now))


bot.run(os.getenv("TOKEN"))
