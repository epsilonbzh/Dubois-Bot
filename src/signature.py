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


def check_signed(user_sws: UserSWS) -> str:
    return "✅" if user_sws.has_signed() else "❌"


def signe(user_sws: UserSWS) -> str:
    res = "❌"

    if user_sws.has_signed():
        res = "☑"
    else:
        user_sws.signature()
        if user_sws.has_signed():
            res = "✅"

    return res


async def signall_c(ctx):
    await ctx.send("Signing in progress")

    embed = discord.Embed(color=0xe67e22)
    embed.title = "Signature send"

    try:
        users = load_users()

        for key, value in users.items():
            if value.get_autosign():
                res = signe(user_sws=value)
                embed.add_field(name=value.get_name(), value=res, inline=False)

    except Exception as err:
        await ctx.send(err)

    await ctx.send(embed=embed)
    await ctx.send("all signatures done")


async def saveme_c(ctx):
    try:
        users = load_users()

        for key, value in users.items():
            if ctx.message.author.id == int(key):
                value.save()
                await ctx.send("<@" + str(ctx.message.author.id) + "> ouf on a eu chaud")

    except Exception as err:
        await ctx.send(err)


async def signme_c(ctx):
    embed = discord.Embed(color=0xe67e22)
    embed.title = "Who signed"

    try:
        users = load_users()

        for key, value in users.items():
            if ctx.message.author.id == int(key):
                res = signe(user_sws=value)
                embed.add_field(name=value.get_name(), value=res)


    except Exception as err:
        await ctx.send(err)

    await ctx.send(embed=embed)


async def whosigned_c(ctx):
    embed = discord.Embed(color=0xe67e22)
    embed.title = "Who signed"

    try:
        users = load_users()

        for key, value in users.items():
            res = check_signed(user_sws=value)
            embed.add_field(name=value.get_name(), value=res, inline=False)

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
