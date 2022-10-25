import random
import discord
from discord.ext import commands
from signature import signmeC, signallC, addautosignC, removeautosignC, listautosignC

admins = [eval(i) for i in open("data/admins.txt", "r").readlines()]

class Commands(commands.Cog):
    def __init__(self, bot):
        self.bot: bot

    @commands.command()
    async def help(self, ctx):
        embed = discord.Embed(title="Liste des commandes :", color=0x3498db)
        embed.add_field(name="quote", value="dit une citation", inline=False)
        embed.add_field(name="ping", value="ping le bot", inline=False)
        await ctx.send(embed=embed)

    @commands.command()
    async def ping(self, ctx):
        await ctx.send("pong")

    @commands.command()
    async def quote(self, ctx):
        quotes = open("data/quotes.txt", 'w').readlines()
        choice = random.randint(0, len(quotes) - 1)
        await ctx.send(quotes[choice])

    @commands.command()
    async def signall(self, ctx):
        if ctx.author.id in admins:
            await signallC(ctx)
        else:
            await ctx.send("Nope")

    @commands.command()
    async def addautosign(self, ctx):
        await addautosignC(ctx,str(ctx.author.id))

    @commands.command()
    async def removeautosign(self, ctx):
            await removeautosignC(ctx, str(ctx.author.id))

    @commands.command()
    async def listautosign(self, ctx):
            await listautosignC(ctx)

    @commands.command()
    async def signme(self, ctx):
        await signmeC(ctx)


async def setup(bot):
    await bot.add_cog(Commands(bot))
