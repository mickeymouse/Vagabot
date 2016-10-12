import discord
import asyncio

from configs import Configs
from Bot import commands

client = discord.Client()

@client.event
@asyncio.coroutine 
def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')

@client.event
@asyncio.coroutine 
def on_message(message):
    for (commandNames, handler, _) in commands.commandList :
        for commandName in commandNames.split() :
            if message.content.startswith(commandName):
                yield from handler(message, client)
            
client.run(Configs['token'])
