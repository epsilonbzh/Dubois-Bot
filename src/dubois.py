import asyncio

import discord
from discord.ext import commands, tasks
from datetime import datetime, time
from signature import signallC

token = open("token.txt", "r").readlines()[0]

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='/', intents=intents, help_command=None)
target_channel_id = 1032901511132487713

hourSign = [time.fromisoformat('00:00:00')]
# hourSign = [time.fromisoformat('08:21:00')]
weekday = datetime.today().weekday()

if {0, 1, 2, 4}.__contains__(weekday):
    hourSign.append(time.fromisoformat('06:00:00'))
    hourSign.append(time.fromisoformat('07:45:00'))
    hourSign.append(time.fromisoformat('09:30:00'))
if {0, 1, 2, 3, 4}.__contains__(weekday):
    hourSign.append(time.fromisoformat('12:00:00'))
    hourSign.append(time.fromisoformat('13:45:00'))

@tasks.loop(time=hourSign)
# @tasks.loop(seconds=1)
async def autosign():
    message_channel = bot.get_channel(target_channel_id)
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
