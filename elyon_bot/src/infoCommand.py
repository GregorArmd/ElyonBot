from warnings import resetwarnings
import discord
from datetime import datetime
from config.db import cursor, connection

def formatString(string):
    string = str(string)
    string = string.replace("(", "")
    string = string.replace(")", "")
    string = string.replace("'", "")
    string = string.split(", ")
    for i in range(len(string)):
        if i > 1 and i != 5 :
            string[i] = int(string[i])
    return string

#async def get_avatar(message, member:discord.Member):
#    show_avat = discord.Embed(color = discord.Colord.dark_blue())
#    show_avat.set_image(url='{}'.format(member.avatar_url))
#    await message.channel.send(embed=show_avatar)

async def printMessage(message, array, client):
    embed = discord.Embed(title = "Stats", description = f"{array[1]}'s Stats.<:Blank:876906223977513011><:Blank:876906223977513011><:Blank:876906223977513011><:Blank:876906223977513011> {array[5]}", color                               = 0x1D068F) #replace message.author by sql name in descritpion
    embed.set_author(name = message.author, icon_url = message.author.avatar_url)
    embed.set_thumbnail(url = client.user.avatar_url)
    embed.add_field(name = "\u200B", value = "\u200B", inline = False)
    embed.add_field(name = ":trophy: Gearscore<:Blank:876906223977513011><:Blank:876906223977513011><:Blank:876906223977513011>", value = array[2], inline = True)
    embed.add_field(name = ":crossed_swords: level<:Blank:876906223977513011><:Blank:876906223977513011><:Blank:876906223977513011><:Blank:876906223977513011>", value = array[3], inline = True)
    embed.add_field(name = ":medal: SP", value = array[4], inline = True)
    embed.add_field(name = "<:red_rune:880084950647463959> Assault", value = array[6], inline = True)
    embed.add_field(name = "<:orange_rune:880084950689382501>Control", value = array[7], inline = True)
    embed.add_field(name = "<:yellow_rune:880084950769086484> Fate", value = array[8], inline = True)
    embed.add_field(name = "<:green_rune:880084950588727297> Support", value = array[10], inline = True)
    embed.add_field(name = "<:blue_rune:880084950743941170> Protection", value = array[9], inline = True)
    embed.add_field(name = "<:purple_rune:880084950697803857>Awakening", value = array[11], inline = True)
    await message.channel.send(embed = embed)
    return 0

async def infoCommand(message, argv, client):
    print("[" + str(datetime.now()) + "] : <" + str(message.author) + "> : <" + str(message.content) + "> :Info command")

    if len(argv) < 3:
        argv = ["&el", "info", "me"]

    if len(argv) > 3:
        await message.channel.send(":x: Too many arguments : expected `&el info` `me` or `name`")
        return -1

    if argv[2] == 'me' :
        res = str(message.author.id)
        sqlCondition = "uuid = '" + res + "'"
    else:
        res = argv[2]
        sqlCondition = "name = '" + res + "'"

    cursor.execute("SELECT name FROM user WHERE " + sqlCondition + ";")
    result = cursor.fetchone()
    if result is None :
        await message.channel.send("No user registered")
        return -1  
    else :
        
        cursor.execute("SELECT uuid, name, u_gear, u_level, u_skill, u_class, r_red, r_orange, r_yellow, r_blue, r_green, r_purple FROM user WHERE " + sqlCondition + ";")
        result2 = formatString(cursor.fetchone())
        print("[" + str(datetime.now()) + "] : <" + str(message.author) + "> :-->", result2)
        return await printMessage(message, result2, client)
