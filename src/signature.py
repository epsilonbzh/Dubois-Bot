import json

from UserSWS import UserSWS


def loaddata():
    f = open("data/signature.json")
    return json.load(f)


async def sign(ctx, config=0):
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
    await sign(ctx, 0)
    await ctx.send("all signatures done")


async def signmeC(ctx):
    await sign(ctx, 1)


async def changeautosigne(ctx, id, state):
    try:
        data = loaddata()

        for etablisement in data:
            for user in etablisement["users"]:
                if (user["id"] == id):
                    user["autosign"] = state

        json_object = json.dumps(data, indent=4)

        with open("data/signature.json", "w") as outfile:
            await ctx.send("toto")
            outfile.write(json_object)

        await ctx.send("<@" + id + ">" + " set " + str(state) + " to autosign")
    except Exception as err:
        await ctx.send(err)

async def removeautosignC(ctx, id):
    await changeautosigne(ctx,id,False)

async def listautosignC(ctx):
    try:
        data = loaddata()
        await ctx.send("toto")
        for etablisement in data:
            for user in etablisement["users"]:
                # await ctx.send(user)
                await ctx.send("<@" + user["id"] + ">" + " at " + str(user["autosign"]))
    except Exception as err:
        await ctx.send(err)

async def addautosignC(ctx, id):
    await changeautosigne(ctx,id,True)
