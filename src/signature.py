import json

import discord

from UserSWS import UserSWS


def loaddata():
    f = open("data/signature.json")
    return json.load(f)


async def signC(ctx, idUser = -1, signe : bool = False):
    embed = discord.Embed(color=0xe67e22)
    if signe:
        embed.title = "Signature send"
    else:
        embed.title = "Who signed"

    data = loaddata()

    for etablisement in data:
        for user in etablisement["users"]:
            name = user["name"]
            if idUser == int(user["id"]):
                name += " (toi)"
            value = "❌"

            try:
                if not signe or (user["autosign"] == True and idUser == -1) or (idUser == int(user["id"])):

                    userSWS = UserSWS(codeEtablisement=etablisement["codeEtablisement"],
                                      codeIdentifiant=user["code_identifiant"],
                                      codePin=user["code_pin"])

                    if signe:
                        if (user["autosign"] == True and idUser == -1) or (idUser == int(user["id"])):
                            if userSWS.hasSigned():
                                value="☑"
                            else:
                                userSWS.signature()
                                if userSWS.hasSigned():
                                    value="✅"
                    else:
                        if userSWS.hasSigned():
                            value ="✅"
                    embed.add_field(name=name, value=value, inline=False)
                else:
                    continue
            except Exception as err:
                print(err)
                await ctx.send(err)


    await ctx.send(embed=embed)


async def signallC(ctx):
    await ctx.send("Signing in progress")
    await signC(ctx,signe=True)
    await ctx.send("all signatures done")


async def signmeC(ctx):
    await signC(ctx, ctx.message.author.id,signe=True)


async def whoSignedC(ctx):
    await signC(ctx, ctx.message.author.id)


async def autosigneC(ctx, idDiscord, state):
    try:
        data = loaddata()

        for etablisement in data:
            for user in etablisement["users"]:
                if user["id"] == idDiscord:
                    user["autosign"] = state

        json_object = json.dumps(data, indent=4)

        with open("data/signature.json", "w") as outfile:
            outfile.write(json_object)

        await ctx.send("<@" + idDiscord + ">" + " set " + str(state) + " to autosign")
    except Exception as err:
        await ctx.send(err)

async def listautosignC(ctx,embed):
    try:
        data = loaddata()
        for etablisement in data:
            for user in etablisement["users"]:
                if ctx.author.id == int(user["id"]):
                    embed.add_field(name=user["name"] + " (toi)", value=("❌","✅")[user["autosign"]], inline=False)
                else:
                    embed.add_field(name=user["name"], value=("❌","✅")[user["autosign"]], inline=False)
    except Exception as err:
        await ctx.send(err)
    return embed

