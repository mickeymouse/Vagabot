import asyncio
import discord
import pickle
from Decorators.singleton import Singleton
from Decorators import authorized

@Singleton
class Setter :
    """This class contains methods that can allow the owner of a server to set up the bot for their usage."""
    def __init__(self, client) :
        self.path = "Ressources/configs.pkl"
        self.load()
        if self.configs is None :
            self.configs = dict()
            for server in client.servers :
                self.configs[server] = dict()
                self.configs[server]['announcement'] = server.default_channel #set the announcement channel by default to the default channel
            self.save()

    def load(self) :
        try :
            with open(self.path, "rb") as f :
                self.configs = pickle.load(f)
        except Exception :
            self.configs = None

    def save(self) :
        with open(self.path, "wb") as f :
            pickle.dump(self.configs, f, pickle.HIGHEST_PROTOCOL)

    @asyncio.coroutine
    def set_announcement(self, message, client) :
        """Set the announcement channel of the server"""
        if message.channel.is_private :
            yield from client.send_message(message.channel, "Vous ne pouvez pas utiliser cette commande sur un salon privé...")
        elif len(message.channel_mentions) == 0 :
            yield from client.send_message(message.channel,  "Utilisation !annonce <mention du salon d'annonce>.")
        else :
            self.configs[message.server]['announcement'] = message.channel_mentions[0]
            self.save()
            yield from client.send_message(message.channel, "Modification du salon d'annonces effectuée !")
