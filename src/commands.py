import random

import discord
from discord.ext import commands
from UserSWS import UserSWS

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
        quotes = open("data/quotes.txt","r").readlines()
        choice = random.randint(0,len(quotes) - 1)
        await ctx.send(quotes[choice])
       
@commands.command()
    async def signe(self, ctx):
        await ctx.send("Signing in progress")
        f = open("data/signature.json")

        data = json.load(f)
        for idUser in data:
            res = "<@" + data[idUser]["discord"] + ">" + " error unable to sign"

            try:
                user = UserSWS(codeEtablisement=data[idUser]["code_etablisement"],
                               codeIdentifiant=data[idUser]["code_identifiant"],
                               codePin=data[idUser]["code_pin"], urlImage=data[idUser]["url_img"],
                               discord=data[idUser]["discord"])

                if user.hasSigned():
                    res = "<@" + data[idUser]["discord"] + ">" + " signature send"
            except Exception as err:
                await ctx.send(err)

            await ctx.send(res)

        await ctx.send("all signatures done")

async def setup(bot):
    await bot.add_cog(Commands(bot))
