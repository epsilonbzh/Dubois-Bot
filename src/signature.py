import json

import discord

from UserSWS import UserSWS


def load_data():
    f = open("data/signature.json")
    return json.load(f)


def load_users() -> dict:
    data = load_data()
    users_sws = dict()

    for etablisement in data:
        for user in etablisement["users"]:
            users_sws[user["id"]] = UserSWS(user["name"], code_etablisement=etablisement["codeEtablisement"],
                                            code_identifiant=user["code_identifiant"],
                                            code_pin=user["code_pin"], autosign=user["autosign"])

    return users_sws


async def signall_c(ctx):
    await ctx.send("Signing in progress")

    embed = discord.Embed(color=0xe67e22)
    embed.title = "Signature send"

    try:
        users = load_users()

        for key, user_sws in users.items():
            if user_sws.get_autosign():
                res = user_sws.signe()
                embed.add_field(name=user_sws.get_name(), value=res, inline=False)

    except Exception as err:
        await ctx.send(err)

    await ctx.send(embed=embed)
    await ctx.send("all signatures done")


async def signme_c(ctx):
    embed = discord.Embed(color=0xe67e22)
    embed.title = "Sign me"

    try:
        users = load_users()

        for key, user_sws in users.items():
            if ctx.message.author.id == int(key):
                res = user_sws.signe()
                embed.add_field(name=user_sws.get_name(), value=res)


    except Exception as err:
        await ctx.send(err)

    await ctx.send(embed=embed)

async def saveme_c(ctx):
    try:
        users = load_users()

        for key, value in users.items():
            if ctx.message.author.id == int(key):
                value.save()
                with open('data/save_warning.png', 'rb') as f:
                    picture = discord.File(f)
                    await ctx.send("<@" + str(ctx.message.author.id) + "> ouf on a eu chaud",file=picture)

    except Exception as err:
        await ctx.send(err)

async def justifyme_c(ctx):
    try:
        users = load_users()

        for key, value in users.items():
            if ctx.message.author.id == int(key):
                value.justify()
                with open('data/justify_warning.png', 'rb') as f:
                    picture = discord.File(f)
                    await ctx.send("<@" + str(ctx.message.author.id) +">",file=picture)

    except Exception as err:
        await ctx.send(err)


async def whosigned_c(ctx):
    embed = discord.Embed(color=0xe67e22)
    embed.title = "Who signed"

    try:
        users = load_users()

        for key, user_sws in users.items():
            res = user_sws.check_signed()
            embed.add_field(name=user_sws.get_name(), value=res, inline=False)

    except Exception as err:
        await ctx.send(err)

    await ctx.send(embed=embed)


async def autosigne_c(ctx, id_discord, state):
    try:
        data = load_data()

        for etablisement in data:
            for user in etablisement["users"]:
                if user["id"] == id_discord:
                    user["autosign"] = state

        json_object = json.dumps(data, indent=4)

        with open("data/signature.json", "w") as outfile:
            outfile.write(json_object)

        await ctx.send("<@" + id_discord + ">" + " set " + str(state) + " to autosign")
    except Exception as err:
        await ctx.send(err)


async def listautosign_c(ctx, embed):
    try:
        data = load_data()
        for etablisement in data:
            for user in etablisement["users"]:
                if ctx.author.id == int(user["id"]):
                    embed.add_field(name=user["name"] + " (toi)", value=("❌", "✅")[user["autosign"]], inline=False)
                else:
                    embed.add_field(name=user["name"], value=("❌", "✅")[user["autosign"]], inline=False)
    except Exception as err:
        await ctx.send(err)
    return embed
