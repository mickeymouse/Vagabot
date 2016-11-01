import discord
import asyncio

from configs import Configs
from Bot import commands
from Bot.setter import Setter
from Bot.beer import Beer

client = discord.Client()

@client.event
@asyncio.coroutine 
def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')
    #initiate the settings
    Setter(client)
    beer = Beer(client)
    
@client.event
@asyncio.coroutine 
def on_message(message):
    command = message.content.split()
    if len(command) > 0 and message.author != client.user :
        command = command[0]
        for (commandNames, handler, _) in commands.commandList :
            for commandName in commandNames.split() :
                if commandName == command :
                    yield from handler(message, client)
            
@client.event
@asyncio.coroutine
def on_member_join(member) :
    setter = Setter()
    nick = member.nick
    if nick is None :
        nick = member.name
    yield from client.send_message(setter.configs[member.server]['announcement'], "Mesdames, Messieurs, veuillez tous acceuillir " + nick + " qui vient de nous rejoindre !")

@client.event
@asyncio.coroutine
def on_member_remove(member) :
    setter = Setter()
    nick = member.nick
    if nick is None :
        nick = member.name
    yield from client.send_message(setter.configs[member.server]['announcement'], "Je vous annonce une triste nouvelle, " + nick + " vient de nous quitter.")

@client.event
@asyncio.coroutine
def on_member_update(before, after) :
    """This event is for the moment only used if a member start streaming."""
    serv = after.server
    setter = Setter()
    if before.game is None :
        stream_before = -1
    else :
        stream_before = before.game.type
    if after.game is None :
        stream_after = -1
    else :
        stream_after = after.game.type

    if stream_before != stream_after and stream_after == 1 :
        nick = after.nick
        if nick is None :
            nick = after.name
        yield from client.send_message(setter.configs[serv]['announcement'], nick + " a commencé un stream, vous pouvez le suivre sur " + after.game.url)

client.run(Configs['token'])
