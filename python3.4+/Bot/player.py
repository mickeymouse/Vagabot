import discord
import asyncio
from Bot import ytsearch
from Decorators import authorized

class Player :
    def __init__(self) :
        self.ytPlayer = None
        self.playList = list()
        self.voice = None
    
    @asyncio.coroutine
    def addToPlaylist(self, ytlink, voiceChannel, client, channel) :
        #if not voiceChannel.permissions_for(client.user).connect :
            #client.send_message(channel, 'Impossible de se connecter sur ce salon vocal...')
            #return None
        me = channel.server.me #now I know who I am in da server !
        perm = voiceChannel.permissions_for(me)
        if not perm.connect :
            yield from client.send_message(channel, "Il m'est impossible de me connecter sur ce salon vocal...")
        elif (ytlink, voiceChannel) in self.playList :
            yield from client.send_message(channel, 'Cette musique est déjà dans la playlist veuillez patienter...')
        else :
            self.playList.append( (ytlink, voiceChannel) )
            yield from client.send_message(channel, 'La musique vient d\'être ajoutée !!!')

    @authorized.require_non_private    
    @asyncio.coroutine
    def play(self, client, server) :
        if len(self.playList) > 0 :
            if not client.is_voice_connected(server) :
                self.voice = yield from client.join_voice_channel(self.playList[0][1])
            else : #In this case, the function has already been called somewhere so we just stop here.
                return None
        while len(self.playList) > 0 and self.voice is not None :
            if self.voice is not None :
                self.ytPlayer = yield from self.voice.create_ytdl_player(self.playList[0][0], use_avconv=True)
            self.ytPlayer.pause()
            self.ytPlayer.start()
            yield from asyncio.sleep(1) #wait a bit of yt loading :p
            self.ytPlayer.resume()
            while self.ytPlayer is not None and not self.ytPlayer.is_done() :
                yield from asyncio.sleep(1)
            while len(self.playList) > 1 and self.playList[0][1] != self.playList[1][1] and len(self.playList[1][1].voice_members) <= 0 :
                self.playList.pop(1)
            if len(self.playList) > 1 and self.playList[0][1] != self.playList[1][1] and self.voice is not None :
                yield from self.voice.move_to(self.playList[1][1])
            if len(self.playList) > 0 :
                self.playList.pop(0)
        self.ytPlayer = None
        if self.voice is not None :
            yield from self.voice.disconnect()

    @authorized.require_non_private
    @asyncio.coroutine
    def pause(self, message, client) :
        if self.ytPlayer is not None :
            yield from client.send_message(message.channel, 'Mise en pause de l\'écoute en cours.')
            self.ytPlayer.pause()
        else :
            yield from cliend.send_message(message.channel, 'Aucune musique en cours d\'écoute.')

    @authorized.require_non_private
    @asyncio.coroutine
    def resume(self, message, client) :
        if self.ytPlayer is not None :
            yield from client.send_message(message.channel, 'Reprise de l\'écoute en cours.')
            self.ytPlayer.resume()
        else :
            yield from client.send_message(message.channel, 'Aucune musique en cours d\'écoute.')

    @authorized.require_non_private
    @asyncio.coroutine
    def title(self, message, client) :
        if self.ytPlayer is None :
            yield from client.send_message(message.channel, 'Aucune musique en cours d\'écoute.')
        else :
            yield from client.send_message(message.channel, 'Écoute en cours : '+self.ytPlayer.title)

    @authorized.require_non_private
    @asyncio.coroutine
    def skip(self, message, client) :
        if self.ytPlayer is not None :
            self.ytPlayer.stop()
            yield from client.send_message(message.channel, 'La musique vient d\'être passée.')
        else :
            yield from client.send_message(message.channel, 'Il n\'y a actuellement aucune musique dans la playlist.')

    @authorized.require_non_private
    @asyncio.coroutine
    def coffee(self, message, client) :
        voiceChannel = message.author.voice.voice_channel
        if voiceChannel is not None :
            yield from self.addToPlaylist('https://www.youtube.com/watch?v=5Y7ZZsOS4O4', voiceChannel, client, message.channel)
            yield from self.play(client, message.server)
        else :
            yield from client.send_message(message.channel, 'Il faut être connecté à un salon vocal pour pouvoir utiliser cette commande.')

    @authorized.require_non_private
    @asyncio.coroutine
    def nosleep(self, message, client) :
        voiceChannel = message.author.voice.voice_channel
        if voiceChannel is not None :
            yield from self.addToPlaylist('https://www.youtube.com/watch?v=07Y0cy-nvAg', voiceChannel, client, message.channel)
            yield from self.play(client, message.server)
        else :
            yield from client.send_message(message.channel, 'Il faut être connecté à un salon vocal pour pouvoir utiliser cette commande.')

    @authorized.require_non_private
    @asyncio.coroutine
    def stop(self, message, client) :
        if self.voice is None :
            yield from client.send_message(message.channel, 'Je ne suis pas connecté sur un salon vocal...')
        else :
            if self.ytPlayer is not None :
                self.ytPlayer.stop()
                self.ytPlayer = None
            self.playList.clear()
            yield from self.voice.disconnect()
            self.voice = None
            yield from client.send_message(message.channel, 'Déconnexion du salon vocal accomplie.')

    @authorized.require_non_private
    @asyncio.coroutine
    def searchAndPlay(self, message, client) :
        ltmp = message.content.split()
        if len(ltmp) < 2 :
            client.send_message(message.channel, 'Utilisation : !play <nom de la musique à rechercher>.')
            return None
        ltmp.pop(0)
        query = ' '.join(ltmp)
        ytlink = ytsearch.getFirstResult(query)
        if ytlink is None :
            client.send_message(message.channel, 'Musique non trouvée...')
        else :
            voiceChannel = message.author.voice.voice_channel
            if voiceChannel is not None :
                yield from self.addToPlaylist(ytlink, voiceChannel, client, message.channel)
                yield from self.play(client, message.server)
            else :
                yield from client.send_message(message.channel, 'Il faut être connecté à un salon vocal pour pouvoir utiliser cette commande.')
