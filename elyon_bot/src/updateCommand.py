from config.db import cursor, connection
from datetime import datetime
from .addCommand import USERINFOS_LIST, sanitizeUserInfo
from .infoCommand import infoCommand

# 0 name
# 1 u_gear
# 2 u_level
# 3 u_skill
# 4 u_class can add class if wanted in the aliases
# 5 r_red
# 6 r_orange
# 7 r_yellow
# 8 r_green
# 9 r_blue
# 10 r_purple

FIELD_ALIAS = {
    'name' : 0,
    'gs' : 1,
    'lvl' : 2,
    'level' : 2,
    'sp' : 3,
    'red' : 5,
    'assault' : 5,
    'orange' : 6,
    'control' : 6,
    'yellow' : 7,
    'fate' : 7,
    'green' : 8,
    'support' : 8,
    'blue' : 9,
    'protection' : 9,
    'purple' : 10,
    'awakening' : 10

}

async def updateCommand(message, argv, client):
    if len(argv) < 4:
        await message.channel.send(":x: Not enough arguments : expected `&el update field1 value1 field2 value2 ...`")
        await message.channel.send("expected fields `" + '`, `'.join(FIELD_ALIAS) + "`")
        return -1
    
    updateMessage = ""
    for i in range(len(argv))[3::2]:
        key = argv[i - 1]
        key = key.lower()
        if not key in FIELD_ALIAS.keys():
            await message.channel.send(":x: Wrong keyword `" + key + "`")
            continue

        info = USERINFOS_LIST[FIELD_ALIAS[key]]
        sanitized, error = sanitizeUserInfo(info, argv[i])

        if error != None:
            await message.channel.send(error)
            continue

        sqlReq = "UPDATE user SET " + info[0] + " = " + sanitized + " WHERE uuid = '" + str(message.author.id) + "';"
        if updateMessage == "":
            updateMessage = f"Updated values for {message.author.mention}:\n```"
        updateMessage += f"{argv[i - 1]} = {sanitized}\n"
        #print("SQL: " + sqlReq)
        
        cursor.execute(sqlReq)
        print("[" + str(datetime.now()) + "] : <" + str(message.author) + "> : <" + str(sanitized) + "> : " + info[0] + " updated!")
    
    if updateMessage != "":
        updateMessage += "```"
        connection.commit()
        await message.channel.send(updateMessage)
        await infoCommand(message, ["&el", "info", "me"], client)
