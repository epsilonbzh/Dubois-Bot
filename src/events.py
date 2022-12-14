import random

from discord.ext import commands

class Events(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message):
        print(message.content.upper())
        if message.content.startswith("/") or message.author.bot:
            return
        elif "SQL" in message.content.upper():
            await message.channel.send("https://tenor.com/view/man-drooling-mouth-gif-13239334")
        else:
            choice = random.randint(0, 50)
            if choice == 0 :
                laughts = open("data/laughts.txt", "r").readlines()
                idx = random.randint(0, len(laughts) - 1)
                await message.channel.send(laughts[idx].upper())
        
async def setup(bot):
    await bot.add_cog(Events(bot))