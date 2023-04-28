import asyncio

import discord
from discord.ext import commands, tasks
import time
from datetime import datetime, time
from signature import signall_c

token = open("data/token.txt", "r").readlines()[0]
dateEndOfTorture = datetime(2023, 4, 28, 17, 15)

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='/', intents=intents, help_command=None)
target_channel_id = 1029791023804731392
target_channel_id_endOfTorture = 1065904716405542932

hourSign = [time.fromisoformat('07:15:00'), time.fromisoformat('09:00:00'), time.fromisoformat('10:45:00'),
            time.fromisoformat('13:15:00'), time.fromisoformat('15:00:00')]


@tasks.loop(time=hourSign)
async def autosign():
    message_channel = bot.get_channel(target_channel_id)
    weekday = datetime.today().weekday()

    if {0, 1, 2, 4}.__contains__(weekday) or (
            {0, 1, 2, 3, 4}.__contains__(weekday) and (datetime.today().time() <= time.fromisoformat('11:00:00'))):
        await signall_c(message_channel)

# send message every 10 minutes from now to 28/04/2023 17h15
@tasks.loop(minutes=1)
async def pingEndOfTorture():
    message_channel = bot.get_channel(target_channel_id_endOfTorture)
    if datetime.today() < dateEndOfTorture:
        seconds=(dateEndOfTorture - datetime.today()).seconds
        m, s = divmod(seconds, 60)
        h, m = divmod(m, 60)
        if h==0:
            await message_channel.send(f'Il reste {m:02d} minutes et {s:02d} secondes')
        if m == 0:
            await message_channel.send(f'Il reste {s:02d} secondes')
        else:
            await message_channel.send(f'Il reste {h:02d} heures, {m:02d} minutes et {s:02d} secondes')
        await message_channel.send("https://media.tenor.com/MH0ziTog4eYAAAAd/homelander-the-boys-season3.gif")
    else:
        await message_channel.send("https://media.tenor.com/gUc8oy81HkgAAAAC/thats-all-folks-ending.gif")
        pingEndOfTorture.stop()
# event at 28/04/2023 17h15


@autosign.before_loop
async def before():
    await bot.wait_until_ready()
    message_channel = bot.get_channel(target_channel_id)
    await message_channel.send("autosign starting")

@pingEndOfTorture.before_loop
async def before():
    if datetime.today() > dateEndOfTorture:
        pingEndOfTorture.stop()
        return
    await bot.wait_until_ready()
    message_channel = bot.get_channel(target_channel_id)
    await message_channel.send("pingEndOfTorture starting")
async def main():
    async with bot:
        await bot.load_extension('events')
        await bot.load_extension('commands')
        pingEndOfTorture.start()
        autosign.start()
        await bot.start(token)


asyncio.run(main())
