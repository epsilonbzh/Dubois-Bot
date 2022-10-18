import asyncio

import discord
from discord.ext import commands

token = open("token.txt","r").readlines()[0]

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='/', intents=intents, help_command=None)

async def main():
    async with bot:
        await bot.load_extension('commands')
        await bot.start(token)

asyncio.run(main())
