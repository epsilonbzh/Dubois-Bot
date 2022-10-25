import json

from src.UserSWS import UserSWS

def loaddata():
    f = open("../data/signature.json")
    return json.load(f)

async def sign(ctx, config = 0):
    data = loaddata()

    for etablisement in data:
        for user in etablisement["users"]:
            res = "<@" + user["id"] + ">" + " error unable to sign"
            try:
                if (user["autosign"] == True and config == 0) or ( str(ctx.message.author.id) == user["id"] and config == 1):
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
        await sign(ctx,0)
        await ctx.send("all signatures done")

async def signmeC(ctx):
    await sign(ctx, 1)
