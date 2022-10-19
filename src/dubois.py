import asyncio
import random

import discord
from discord.ext import commands

token = open("token.txt", "r").readlines()[0]

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='/', intents=intents, help_command=None)


async def main():
    async with bot:
        @bot.event
        async def on_message(message):
            choice = random.randint(0, 50)
            if choice == 1 :
                laughts = open("../data/laughts.txt", "r").readlines()
                idx = random.randint(0, len(laughts) - 1)
                await message.channel.send(laughts[idx].upper())

        await bot.load_extension('commands')
        await bot.start(token)


asyncio.run(main())
