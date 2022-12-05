import json

from UserSWS import UserSWS


def loaddata():
    f = open("data/signature.json")
    return json.load(f)


async def signC(ctx, config=0):
    idAuthor = -1
    if (config == 1):
        idAuthor = str(ctx.message.author.id)

    data = loaddata()

    for etablisement in data:
        for user in etablisement["users"]:
            res = "<@" + user["id"] + ">" + " error unable to sign"
            try:

                if (user["autosign"] == True and config == 0) or (idAuthor == user["id"] and config == 1):

                    userSWS = UserSWS(codeEtablisement=etablisement["codeEtablisement"],
                                      codeIdentifiant=user["code_identifiant"],
                                      codePin=user["code_pin"])
                    if userSWS.hasSigned():
                        res = res = "<@" + user["id"] + ">" + " already sign"
                    else:
                        userSWS.signature()
                        if userSWS.hasSigned():
                            res = res = "<@" + user["id"] + ">" + " signature send"
                else:
                    continue

            except Exception as err:
                print(err)
                await ctx.send(err)
            print(res)
            await ctx.send(res)


async def signallC(ctx):
    await ctx.send("Signing in progress")
    await signC(ctx, 0)
    await ctx.send("all signatures done")


async def signmeC(ctx):
    await signC(ctx, 1)


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

