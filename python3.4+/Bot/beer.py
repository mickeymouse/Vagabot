import discord
import asyncio
import time
import random
from Bot.setter import Setter
from Decorators.singleton import Singleton
from Decorators.background import bg_task

@Singleton
class Beer :
    def __init__(self, client) :
        self.maxBeers = 90
        self.lambd = 1/9
        self.drinkConsuptions = dict()
        self.highscores = dict()
        self.capacities = dict()
        self.client = client
        self.flag = False
        for serv in client.servers :
            self.drinkConsuptions[serv] = dict()
            self.highscores[serv] = [None for _ in range(3)]
            self.capacities[serv] = 6 + int(random.expovariate(self.lambd))
            for member in serv.members :
                self.drinkConsuptions[serv][member] = 0
        self.client.loop.create_task(self.decreaseConsuption())
        self.client.loop.create_task(self.getNewBeers())

    def updateHighscore(self, member) :
        serv = member.server
        highscore = self.highscores[serv]
        drinkConsuptions = self.drinkConsuptions[serv]
        i = 0
        for e in highscore :
            if e is None :
                highscore[i] = (member, drinkConsuptions[member])
                break
            if member == e[0] :
                if drinkConsuptions[member] > e[1] :
                    highscore[i] = (member, drinkConsuptions[member])
                break
            i += 1
        if i == 3 : #in this case we have to check if the member beat the highscore at 3rd position
            if drinkConsuptions[member] > highscore[2][1] :
                highscore[2] = (member, drinkConsuptions[member])
                i = 2
            else :
                return None
        while i > 0 and highscore[i][1] > highscore[i-1][1] :
            highscore[i], highscore[i-1] = highscore[i-1], highscore[i]
            i -= 1

    def showAndResetHighscore(self, serv) :
        ret = "Et les plus gros soiffards d'aujourd'hui sont :\n"
        nick = self.highscores[serv][0][0].nick
        if nick is None :
            nick = self.highscores[serv][0][0].name
        ret += "En première position " + nick + " avec un maximum de " + str(self.highscores[serv][0][1]) + " stacks !!!\n"
        if self.highscores[serv][1] is not None :
            nick = self.highscores[serv][1][0].nick
            if nick is None :
                nick = self.highscores[serv][1][0].name
            ret += "En deuxième position " + nick + " avec un maximum de " + str(self.highscores[serv][1][1]) + " stacks !!\n"
        if self.highscores[serv][2] is not None :
            nick = self.highscores[serv][2][0].nick
            if nick is None :
               nick = self.highscores[serv][2][0].name
            ret += "En troisième position " + nick + " avec un maximum de " + str(self.highscores[serv][2][1]) + " stacks !"
        self.highscores[serv] = [None for _ in range(3)]
        return ret

    @bg_task(7200)
    @asyncio.coroutine
    def decreaseConsuption(self) :
        for serv in self.drinkConsuptions :
            for member in self.drinkConsuptions[serv] :
                self.drinkConsuptions[serv][member] = max(self.drinkConsuptions[serv][member]-1, 0)

    @asyncio.coroutine
    def drink(self, message, client) :
        if message.channel.is_private :
            yield from client.send_message(message.channel, "Ce n'est pas bien de picoler en cachette !")
        elif self.capacities[message.server] == 0 :
            yield from client.send_message(message.channel, "Il n'y a plus de stack à disposition, veuillez attendre le réapprovisionnement !")
        else :
            nick = message.author.nick
            if nick is None :
                nick = message.author.name
            self.drinkConsuptions[message.server][message.author] += 1
            self.capacities[message.server] -= 1
            yield from client.send_message(message.channel, nick + " vient de consommer une stack ! Il en est actuellement à un total de {:d} stacks !".format(self.drinkConsuptions[message.server][message.author]))
            self.updateHighscore(message.author)

    @bg_task()
    @asyncio.coroutine
    def getNewBeers(self) :
        setter = Setter()
        lt = time.localtime(None)
        if lt.tm_hour == 0 and not self.flag :
            self.flag = True
            for serv in self.client.servers :
                self.capacities[serv] += 6 + int(random.expovariate(self.lambd))
                if self.capacities[serv] > self.maxBeers :
                    self.capacities[serv] = self.maxBeers
                if self.highscores[serv][0] is not None :
                    message = self.showAndResetHighscore(serv)
                    yield from self.client.send_message(setter.configs[serv]['announcement'], message)
                yield from self.client.send_message(setter.configs[serv]['announcement'], "Réapprovisionnement de stacks effectué !")
        if lt.tm_hour == 1 and self.flag :
            self.flag = False
