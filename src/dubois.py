import asyncio

import discord
from discord.ext import commands, tasks
import time
from datetime import datetime, time
from signature import signallC

token = open("data/token.txt", "r").readlines()[0]

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='/', intents=intents, help_command=None)
target_channel_id = 1029791023804731392

hourSign = [time.fromisoformat('07:15:00'), time.fromisoformat('9:00:00'), time.fromisoformat('10:45:00'),
            time.fromisoformat('13:15:00'), time.fromisoformat('15:00:00')]
# hourSign = [time.fromisoformat('06:00:00'),time.fromisoformat('12:00:00')]
# hourSign = [time.fromisoformat('06:45:00'), time.fromisoformat('11:45:00')]


@tasks.loop(time=hourSign)
async def autosign():
    message_channel = bot.get_channel(target_channel_id)
    weekday = datetime.today().weekday()

    if {0, 1, 2, 4}.__contains__(weekday) or (
            {0, 1, 2, 3, 4}.__contains__(weekday) and (datetime.today().time() <= time.fromisoformat('11:00:00'))):
        await signallC(message_channel)


@autosign.before_loop
async def before():
    await bot.wait_until_ready()
    message_channel = bot.get_channel(target_channel_id)
    await message_channel.send("autosign starting")


async def main():
    async with bot:
        await bot.load_extension('events')
        await bot.load_extension('commands')
        autosign.start()
        await bot.start(token)


asyncio.run(main())
