from config.db import cursor, connection
from datetime import datetime
import asyncio
from .infoCommand import infoCommand
from threading import Timer,Thread,Event

activeAddingUsers = {}

# [sqlname, type, asking sentence, metadata]
USERINFOS_LIST = [
    ["name", "string", "You have 5 min to answer all questions\nWhat is your main character name", 3, 20],
    ["u_gear", "int", "What is your main character Item Level", 0, 1500],
    ["u_level", "int", "What is your main character level", 0, 100],
    ["u_skill", "int", "What is your main character number of skill points", 0, 1500],
    ["u_class", "choice", "What is your main character class (slayer/elem/assa/warlord/gunner/mystic)", ["slayer", "elem", "assa", "warlord", "gunner", "mystic"]],
    ["r_red", "int", "What is your main character Assault rune number ", 0, 100],
    ["r_orange", "int", "What is your main character Control rune number ", 0, 100],
    ["r_yellow", "int", "What is your main character Fate rune number ", 0, 100],
    ["r_green", "int", "What is your main character Support rune number ", 0, 100],
    ["r_blue", "int", "What is your main character Protection rune number ", 0, 100],
    ["r_purple", "int", "What is your main character Awakening rune number ", 0, 100]
]

def sanitizeUserInfo(info, value):
    if info[1] == "string":
        if value.isalnum() == False:
            return ["", ":x: Wrong input retry only letters and numbers"]
        if len(value) < info[3] or len(value) > info[4]:
            return ["", ":x: Wrong input out of range : min `"+ str(info[3]) + "` max `" +str(info[4]) + "`"]
        return ["'" + value + "'", None]

    elif info[1] == "int":           
        try:
            contentint = int(value)
        except ValueError :
            return ["", ":x: Wrong input retry only numbers"]
        if contentint < info[3] or contentint > info[4]:
            return ["", ":x: Wrong input out of range : min `"+ str(info[3]) + "` max `" +str(info[4]) + "`"]
        return [str(contentint), None]

    elif info[1] == "choice":
        lowered=value.lower()
        shortcuts = {
            "elementalist": "elem",
            "assassin": "assa",
            "war": "warlord",
            "gun": "gunner",
            "slay": "slayer"
        }
        if lowered in shortcuts.keys():
            lowered = shortcuts[lowered]
        if lowered in info[3]:
            return ["'" + lowered + "'", None]
        else:
            return ["", ":x: That class is not in the game " + str(info[3])]
    else:
        return [value, "Sorry on code avec des noobs"]


class UserAdderState:
    def __init__(self, channel, author, client):
        self.channel = channel
        self.author = author
        self.infos = []
        self.client = client
        self.timeouter = Timer(300, self.timeoutHandler)
        self.timeouter.start()
    
    async def addInfoFromMessage(self, message):
        # Check incoming info
        currentInfo = USERINFOS_LIST[len(self.infos)]
        sanitized, error = sanitizeUserInfo(currentInfo, message.content)
        if error != None:
            await message.channel.send(error)
            return True

        # Add info to our table
        self.infos.append(sanitized)
        if len(self.infos) >= len(USERINFOS_LIST):
            # use all infos to add user in db
            self.timeouter.cancel()
            self.saveToDB()
            await infoCommand(message, ["&el", "info", "me"], self.client)
            del activeAddingUsers[self.author.id]
            return True
        await self.printNextExpectation(message.channel, message.author)
        return True
    
    async def printNextExpectation(self, channel, author):
        currentInfo = USERINFOS_LIST[len(self.infos)]
        await channel.send(f"{author.mention}" + currentInfo[2])
    
    def saveToDB(self):
        # "INSERT INTO user (uuid,"
        sqlReq = "INSERT INTO user(uuid, "
        # name, u_gear, u_level, u_skill, u_class, r_red, r_orange, r_yellow, r_green, r_blue, r_purple
        sqlReq += ', '.join(map(lambda v: v[0], USERINFOS_LIST))
        # ") VALUES ('" + str(message.author.id) + "',
        sqlReq += ") VALUES ('" + str(self.author.id) + "', "
        # '" + name.content +"', " + u_gear.content + ", " + u_level.content + ", " + u_skill.content + ", '" + u_class.content + "' , " + r_red.content + ", " + r_orange.content + ", " + r_yellow.content + ", " + r_green.content + "," + r_blue.content + ", " + r_purple.content + 
        sqlReq += ', '.join(self.infos)
        # ");")
        sqlReq += ");"
        cursor.execute(sqlReq)
        connection.commit()

    def timeoutHandler(self):
        #asyncio.run(self.channel.send("Trop lent, timeouted " + self.author.mention))
        print(f":x: User {self.author.mention} got timed out when adding")
        del activeAddingUsers[self.author.id]

async def handleMessageForAddingUser(message):
    if message.author.id in activeAddingUsers.keys():
        return await activeAddingUsers[message.author.id].addInfoFromMessage(message)
    return False

# &el add
async def addCommand(message, argv, client):
    print("[" + str(datetime.now()) + "] : <" + str(message.author) + "> : Add Command")
    cursor.execute("SELECT uuid FROM user WHERE uuid = '" + str(message.author.id) + "';")
    result = cursor.fetchone()
    if result is not None : 
        await message.channel.send(":x: User already registered")
        return 0
    newUser = UserAdderState(message.channel, message.author, client)
    activeAddingUsers[message.author.id] = newUser
    await newUser.printNextExpectation(message.channel, message.author)