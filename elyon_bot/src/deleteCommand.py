from config.db import cursor, connection
import asyncio
from datetime import datetime

async def deleteCommand(message, argv, client):
    print("[" + str(datetime.now()) + "] : <" + str(message.author) + "> : <" + str(message.content) + "> : delete Command")

    
    if len(argv) < 3:
        await message.channel.send("Not enough arguments : expected `&el delete` `me` / `id`")
        return -1
    if len(argv) > 3:
        await message.channel.send("Too many arguments : expected `&el delete` `me` / `id`")
        return -1

    if argv[2] == 'me' or argv[2] == str(message.author.id):
        id = str(message.author.id)
    else:
        if str(message.author.id) == "194770593474674688" or str(message.author.id) == "166153934841446400": 
            id = argv[2]
        else :
            return await message.channel.send(":x: Permission denied")

    cursor.execute("SELECT uuid FROM user WHERE uuid = '" + id + "';")
    result = cursor.fetchone()

    if result is None :
        await message.channel.send("No user registered")
        return -1
    else :
        cursor.execute("DELETE FROM user WHERE uuid = '" + id + "';")
        connection.commit()
        await message.channel.send("User deleted")
        return 0
