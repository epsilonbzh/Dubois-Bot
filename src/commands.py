import random
import discord
from discord.ext import commands
from signature import signmeC, signallC, listautosignC, autosigneC, whoSignedC, savemeC

admins = [eval(i) for i in open("data/admins.txt", "r").readlines()]


class Commands(commands.Cog):
    def __init__(self, bot):
        self.bot: bot

    @commands.command()
    async def help(self, ctx):
        embed = discord.Embed(title="Liste des commandes :", color=0x3498db)
        embed.add_field(name="quote", value="Pit une citation", inline=False)
        embed.add_field(name="ping", value="Ping le bot", inline=False)
        embed.add_field(name="signme", value="Signe sur SWS", inline=False)
        embed.add_field(name="autosignadd", value="Active la signature automatique", inline=False)
        embed.add_field(name="autosignremove", value="Désactive la signature automatique", inline=False)
        embed.add_field(name="autosignlist", value="Liste les personnes inscrites à la signature automatique", inline=False)
        embed.add_field(name="saveme", value="Surprime la signature ou enlève le code pour nous sauver Delphine", inline=False)
        await ctx.send(embed=embed)

    @commands.command()
    async def ping(self, ctx):
        await ctx.send("pong")

    @commands.command()
    async def quote(self, ctx):
        quotes = open("data/quotes.txt", 'r').readlines()
        choice = random.randint(0, len(quotes) - 1)
        await ctx.send(quotes[choice])

    @commands.command()
    async def signall(self, ctx):
        if ctx.author.id in admins:
            await signallC(ctx)
        else:
            await ctx.send("Nope")

    @commands.command()
    async def signme(self, ctx):
        await signmeC(ctx)


    @commands.command()
    async def saveme(self, ctx):
        await savemeC(ctx)

    @commands.command()
    async def whosigned(self, ctx):
        await whoSignedC(ctx)

    @commands.command()
    async def autosignadd(self, ctx):
        await autosigneC(ctx, str(ctx.author.id), True)

    @commands.command()
    async def autosignremove(self, ctx):
        await autosigneC(ctx, str(ctx.author.id), False)

    @commands.command()
    async def autosignlist(self, ctx):
        embed = discord.Embed(title="Auto sign :", color=0xe67e22)
        embed = await listautosignC(ctx, embed)
        await ctx.send(embed=embed)


async def setup(bot):
    await bot.add_cog(Commands(bot))
