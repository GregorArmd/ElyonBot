import os
import discord
import asyncio
from datetime import datetime
from src.split import split_args
from src.addCommand import handleMessageForAddingUser
from dotenv import load_dotenv
import sys
load_dotenv('config/.env')
token = os.getenv('TOKEN')

client = discord.Client()

@client.event
async def on_ready():
    print("Bot is ready !")
    await client.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name="&el help"))
async def handleMessageCommand(message):
    argv = message.content.split()
    if len(argv) == 0:
        return False
    if argv[0] == '&el':
        message.content = ' '.join(argv)
        await split_args(message, argv, client)
        return True
    return False

@client.event
async def on_message(message):
    if (message.channel.name == 'elyon_bot'):
        if await handleMessageForAddingUser(message):
            #print('handled as adding user')
            x=0
        elif await handleMessageCommand(message):
            #print ('handle as command')
            x=0
        #a delete :     
        #else:
        #    print('fuck that ' + str(message.author))

client.run(token)

