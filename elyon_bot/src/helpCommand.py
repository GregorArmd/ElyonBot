import discord
from config.db import cursor, connection
from datetime import datetime

client = discord.Client()

async def helpCommand(message, argv, client):
    embed = discord.Embed(title="Help", description="Helping page", color=0x1D068F)
    embed.set_author(name=client.user.name, icon_url=client.user.avatar_url)
    embed.add_field(name=":white_small_square:`&el help`", value=":heavy_minus_sign: shows this message.", inline=False)
    embed.add_field(name=":white_small_square:`&el add`", value=":heavy_minus_sign: Will ask you a serie of questions concerning your main character.\n:heavy_minus_sign: You have 5 min to answer them all.", inline=False)
    embed.add_field(name=":white_small_square:`&el update` `field1 value1` `field2 value2`", value=":heavy_minus_sign: Updates your main character informations, you can update several fields at the same time. type `&el update` to see all fields.\n:heavy_minus_sign: **exemple** : `&el update gs 450 lvl 48 red 12`", inline=False)
    embed.add_field(name=":white_small_square:`&el list` `gs` / `name` / `class`", value=":heavy_minus_sign: shows a list containing every users name, class, gs, level ordered by gs.", inline=False)
    embed.add_field(name=":white_small_square:`&el info` `me` / `name`", value=":heavy_minus_sign: **me** : shows your main character information in a specific embed\n:heavy_minus_sign: **name** : shows the information concerning the player whose name you typed.", inline=False)
    embed.add_field(name=":white_small_square:`&el delete` `me` / `id`", value=":heavy_minus_sign: **me** : deletes all your character informations\n:heavy_minus_sign: **id** : deletes the informations corresponding to the user ID only available for people having the permissions.", inline=False)
    await message.channel.send(embed=embed)
    print("[" + str(datetime.now()) + "] : <" + str(message.author) + "> : <" + str(message.content) + "> : Help Command")
    return


