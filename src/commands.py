import random
import json

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
        quotes = open("data/quotes.txt", "r").readlines()
        choice = random.randint(0, len(quotes) - 1)
        await ctx.send(quotes[choice])

    @commands.command()
    async def signe(self, ctx):
        try:
            await ctx.send("Signing in progress")
            f = open("../data/signature.json")

            data = json.load(f)
            for etablisement in data:
                for user in etablisement["users"]:
                    res = "<@" + user["id"] + ">" + " error unable to sign"
                    try:
                        if user["autosign"]:
                            userSWS = UserSWS(codeEtablisement=etablisement["codeEtablisement"],
                                              codeIdentifiant=user["code_identifiant"],
                                              codePin=user["code_pin"])

                            if userSWS.hasSigned():
                                res = res = "<@" + user["id"] + ">" + " signature send"
                    except Exception as err:
                        print(err)
                        await ctx.send(err)
                    print(res)
                    await ctx.send(res)

            await ctx.send("all signatures done")
        except Exception as err:
            await ctx.send(err)

    @commands.command()
    async def jesigne(self, ctx):
        try:
            f = open("../data/signature.json")
            idUser = str(ctx.message.author.id)
            data = json.load(f)
            userSWS = -1
            res = "<@" + idUser + ">"
            for etablisement in data:
                for user in etablisement["users"]:
                    if idUser == user["id"]:
                        userSWS = UserSWS(codeEtablisement=etablisement["codeEtablisement"],
                                          codeIdentifiant=user["code_identifiant"],
                                          codePin=user["code_pin"])

                if userSWS == -1:
                    res += str(ctx.message.author) + " not in database, id : " + idUser
                else:
                    if userSWS.hasSigned():
                        res += " signed"
                    else:
                        res += " error unable to sign"
                await ctx.send(res)

        except Exception as err:
            await ctx.send(err)


async def setup(bot):
    await bot.add_cog(Commands(bot))
