import json

import discord

from UserSWS import UserSWS


def load_data():
    f = open("data/signature.json")
    return json.load(f)


async def sign_c(ctx, id_user = -1, signe : bool = False):
    embed = discord.Embed(color=0xe67e22)
    if signe:
        embed.title = "Signature send"
    else:
        embed.title = "Who signed"

    data = load_data()

    for etablisement in data:
        for user in etablisement["users"]:
            name = user["name"]
            if id_user == int(user["id"]):
                name += " (toi)"
            value = "❌"

            try:
                if not signe or (user["autosign"] == True and id_user == -1) or (id_user == int(user["id"])):

                    user_sws = UserSWS(code_etablisement=etablisement["codeEtablisement"],
                                      code_identifiant=user["code_identifiant"],
                                      code_pin=user["code_pin"])

                    if signe:
                        if (user["autosign"] == True and id_user == -1) or (id_user == int(user["id"])):
                            if user_sws.has_signed():
                                value="☑"
                            else:
                                user_sws.signature()
                                if user_sws.has_signed():
                                    value="✅"
                    else:
                        if user_sws.has_signed():
                            value ="✅"
                    embed.add_field(name=name, value=value, inline=False)
                else:
                    continue
            except Exception as err:
                print(err)
                await ctx.send(err)


    await ctx.send(embed=embed)


async def signall_c(ctx):
    await ctx.send("Signing in progress")
    await sign_c(ctx, signe=True)
    await ctx.send("all signatures done")

async def saveme_c(ctx):
    try:
        data = load_data()
        for etablisement in data:
            for user in etablisement["users"]:
                if ctx.message.author.id == int(user["id"]):
                    user_sws = UserSWS(code_etablisement=etablisement["codeEtablisement"],
                                      code_identifiant=user["code_identifiant"],
                                      code_pin=user["code_pin"])
                    user_sws.save()
                    await ctx.send("ok")

    except Exception as err:
        await ctx.send(err)


async def signme_c(ctx):
    await sign_c(ctx, ctx.message.author.id, signe=True)


async def whosigned_c(ctx):
    await sign_c(ctx, ctx.message.author.id)


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
                    embed.add_field(name=user["name"] + " (toi)", value=("❌","✅")[user["autosign"]], inline=False)
                else:
                    embed.add_field(name=user["name"], value=("❌","✅")[user["autosign"]], inline=False)
    except Exception as err:
        await ctx.send(err)
    return embed

