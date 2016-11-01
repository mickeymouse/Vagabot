import discord
import asyncio
import pickle
import random
from KupoParser import parser as KParser
from Bot.player import Player
from Bot.poll import Poll
from Bot.setter import Setter
from Bot.beer import Beer
from Decorators import authorized

@authorized.require_non_private
@asyncio.coroutine
def say(message, client) :
    arg = message.content.split()
    arg.pop(0)
    arg = ' '.join(arg)
    author = message.author
    channel = message.channel
    me = message.server.me
    if channel.permissions_for(me).manage_messages :
        yield from client.delete_message(message)
    if arg != '' :
        yield from client.send_message(channel, arg)
    else :
        try :
            yield from client.send_message(author, 'Que dois-je donc répéter ?')
            msg = yield from client.wait_for_message(timeout=60.0, author=author)
            if msg is None :
                yield from client.send_message(author, 'Je n\'ai pas reçu de réponse veuillez recommencer en utilisant !say.')
            else :
                yield from client.send_message(channel, msg.content)
        except Exception :
            pass
        

@asyncio.coroutine
def printHello(message, client) :
    yield from client.send_message(message.channel, 'Bonjour '+message.author.mention+' !!!')
    
@asyncio.coroutine
def printStatus(message, client) :
    tmp = yield from client.send_message(message.channel, 'Recherche du statut du serveur ...')
    if KParser.isWorldUp() :
        yield from client.edit_message(tmp, 'Le serveur Moogle est actuellement en ligne. :white_check_mark:')
    else :
        yield from client.edit_message(tmp, 'Le serveur Moogle est actuellement hors-ligne. :no_entry_sign:')
        

@asyncio.coroutine
def printNewChar(message, client) :
    tmp = yield from client.send_message(message.channel, 'Recherche concernant la création de personnage sur le serveur ...')
    if KParser.isCharCreatable() :
        yield from client.edit_message(tmp, 'Il est actuellement possible de créer un personnage sur Moogle. :white_check_mark:')
    else :
        yield from client.edit_message(tmp, 'Il est actuellement impossible de créer un personnage sur Moogle. :no_entry_sign:')

@asyncio.coroutine
def registerChar(message, client) :
    query = message.content.split()
    if len(query) < 3 :
        yield from client.send_message(message.channel, 'Utilisation !iam <prénom> <nom>.')
        return None
    tmp = yield from client.send_message(message.channel, 'Recherche du personnage dans le jeu ...')
    try :
        with open('Ressources/characters.pkl', 'rb') as f:
            characters = pickle.load(f)
    except Exception :
        characters = dict()
    query = query[1]+'+'+query[2]
    if KParser.registerCharIn(characters, query, message.author) :
        with open('Ressources/characters.pkl', 'wb') as f:
            pickle.dump(characters, f, pickle.HIGHEST_PROTOCOL)
        yield from client.edit_message(tmp, 'Personnage enregistré !!!')
    else :
        yield from client.edit_message(tmp, 'Ce personnage ne semble pas exister sur le serveur Moogle.')

def showTodoList() :
    try :
        with open('Ressources/todo.pkl', 'rb') as f:
            todo = pickle.load(f)
    except Exception :
        return ''
    if len(todo) == 0 :
        return ''
    display = '**Liste des tâches à accomplir :**\n'
    for i in range(len(todo)) :
        display += ':small_orange_diamond: **n°'+str(i+1)+'**\t'+todo[i]+'\n'
    return display

def addTodoList(whatTodo) :
    try :
        with open('Ressources/todo.pkl', 'rb') as f:
            todo = pickle.load(f)
    except Exception :
        todo = list()
    todo.append(whatTodo)
    with open('Ressources/todo.pkl', 'wb') as f:
        pickle.dump(todo, f, pickle.HIGHEST_PROTOCOL)

@asyncio.coroutine
def todo(message, client) :
    query = message.content.split()
    if len(query) <= 1 : #case where we want to show the list
        display = showTodoList()
        if display == '' :
            yield from client.send_message(message.channel, 'La liste est vide...')
        else :
            yield from client.send_message(message.channel, display)
    else :
        query.pop(0)
        addTodoList(' '.join(query))
        yield from client.send_message(message.channel, 'Tâche ajoutée à la liste !')

@asyncio.coroutine
def removeTodo(message, client) :
    try :
        with open('Ressources/todo.pkl', 'rb') as f:
            todo = pickle.load(f)
    except Exception :
        yield from client.send_message(message.channel, 'La liste est vide...')
        return None
    if len(todo) == 0 :
        yield from client.send_message(message.channel, 'La liste est vide...')
        return None
    query = message.content.split()
    if len(query) < 1 :
        yield from client.send_message(message.channel, 'Utilisation !retirer <numéro de la tâche>')
        return None
    try :
       num = int(query[1]) - 1
    except ValueError :
        yield from client.send_message(message.channel, 'L\'argument doit être un numéro de tâche...')
        return None
    if 0 <= num and num < len(todo) :
        task = todo.pop(num)
        with open('Ressources/todo.pkl', 'wb') as f:
            pickle.dump(todo, f, pickle.HIGHEST_PROTOCOL)
        yield from client.send_message(message.channel, 'La tâche "'+ task + '" a été suprimée !')
    else :
        yield from client.send_message(message.channel, 'L\'argument doit être un numéro de tâche...')

@asyncio.coroutine
def printChar(message, client, member) :
    try :
        with open('Ressources/characters.pkl', 'rb') as f:
            characters = pickle.load(f)
    except Exception :
        yield from client.send_message(message.channel, 'Ce personnage n\'est pas enregistré')
        return None
    if member in characters :
        yield from client.send_message( message.channel, KParser.getCharacterInfo(characters[member][0], characters[member][1]) )
    else :
        yield from client.send_message(message.channel, 'Ce personnage n\'est pas enregistré')
        
@asyncio.coroutine
def charInfo(message, client) :
    if len(message.mentions) > 0 :
        yield from printChar(message, client, message.mentions[0])
    else :
        yield from client.send_message(message.channel, 'Vous n\'avez pas précisé qui vous vouliez rechercher...')
        
@asyncio.coroutine
def authorCharInfo(message, client) :
    yield from printChar(message, client, message.author)

@asyncio.coroutine
def roll(message, client) :
    query = message.content.split()
    nick = message.author.name
    serv = message.server
    channel = message.channel
    if not channel.is_private :
        if message.author.nick is not None :
            nick = message.author.nick
        if channel.permissions_for(serv.me).manage_messages :
            yield from client.delete_message(message)
    if len(query) < 2 :
        yield from client.send_message(channel, nick + ' jette un dé à 100 faces, résultat obtenu ' + str(random.randint(1,100)) + ' !')
    else :
        try :
            b = int(query[1])
            if b < 2 :
                yield from client.send_message(channel, 'le nombre de faces du dé doit être supérieur ou égal à 2...')
            else :
                yield from client.send_message(channel, nick + ' jette un dé à ' + str(min(b,2**64-1)) + ' faces, résultat obtenu ' + str(random.randint(1,min(b,2**64-1))) + ' !')
        except ValueError :
            yield from client.send_message(channel, 'la deuxième valeur n\'est pas un entier...')

@authorized.require_non_private
@authorized.only_owner_top_role
@asyncio.coroutine
def set_announcement(message, client) :
    setter = Setter()
    yield from setter.set_announcement(message, client)

@asyncio.coroutine
def drink(message, client) :
    beer = Beer()
    yield from beer.drink(message, client)

@asyncio.coroutine
def printHelp(message, client) :
    commands_per_message = 20
    i = 0
    msg = 'Mes commandes sont les suivantes :\n'
    for (commandNames, handler, desc) in commandList :
        msg += commandNames + ' : ' + desc + '\n'
        i += 1
        if i == 20 :
            try :
                yield from client.send_message(message.author, msg)
            except Exception :
                pass
            msg = ''
            i = 0
    if i != 0 :
        try :
            yield from client.send_message(message.author, msg)
        except Exception :
            pass
    
player = Player()
poll = Poll()

#list all the commands here in tupple in the format (commandNames, actionHandler, description)
commandList = [ 
    ('!bonjour !hello !salut', printHello, 'Dites moi bonjour et je vous répondrai.'),
    ('!say !dire', say, 'Répète le message passé en argument. Usage !dire\/!say <message>'),
    ('!status', printStatus, 'Permet de savoir l\'état actuel du serveur Moogle.'),
    ('!newchar', printNewChar, 'Permet de savoir s\'il est possible de créer un nouveau personnage sur le serveur Moogle.'),
    ('!iam', registerChar, 'Permet d\'enregistrer son personnage de jeu. Utilisation !iam <Prénom> <Nom>'),
    ('!whois', charInfo, 'Permet d\'afficher les informations d\'un personnage enregistré. Utilisation !whois <@pseudo>'),
    ('!whoami', authorCharInfo, 'Permet d\'afficher les informations concernant votre personnage enregistré.'),
    ('!café !coffee', player.coffee, 'Mise en écoute de **Le Café** de *Oldelaf et Monsieur D* sur le salon vocal.'),
    ('!nosleep', player.nosleep, 'Mise en écoute de **No Sleep Till Brooklyn** de *The Beastie Boys* sur le salon vocal.'),
    ('!play', player.searchAndPlay, 'Ajout dans la playlist de la première vidéo trouvée sur YouTube. Usage : !play <nom de la musique à rechercher>.'),
    ('!skip', player.skip, 'Permet de passer la musique en cours d\'écoute dans la playlist.'),
    ('!titre', player.title, 'Permet d\'afficher le titre en cours d\'écoute.'),
    ('!pause', player.pause, 'Met en pause la lecture en cours.'),
    ('!resume !reprise', player.resume, 'Reprise de la lecture en cours.'),
    ('!stop', player.stop, 'Déconnecte le bot du salon vocal.'),
    ('!todo !àfaire', todo, 'Affiche la liste de choses à faire si aucun argument n\'est utilisé, ajoute l\'argument dans la liste des choses à faire sinon.'),
    ('!retirer', removeTodo, 'Utilisation !retirer <numéro tâche>, retire la tâche, dont le numéro est affiché en faisant !todo/!àfaire sans argument, de la liste.'),
    ('!sondage !poll', poll.setPoll, 'Affiche le sondage en cours si aucun argument n\'est utilisé, crée un sondage avec pour question l\'argument si précisé.'),
    ('!oui !yes', poll.yes, 'Vote oui sur le sondage en cours.'),
    ('!non !no', poll.no, 'Vote non sur le sondage en cours.'),
    ('!avorter !abort', poll.abort, 'Force l\'arrêt du sondage en cours.'),
    ('!roll !dé', roll, 'lance un dé à 100 faces si aucun paramètre n\'est précisé. !roll 42 lance un dé à 42 faces.'),
    ('!annonce', set_announcement, 'Modifie le salon utilisé pour faire les annonces du bot.'),
    ('!stack', drink, 'Ajoute une stack à la personne utilisant cette commande. Nous vous rappelons que l\'abus d\'alcool est dangereux pour la santé !'),
    ('!help', printHelp, 'Affiche la liste des commandes ainsi que leurs descriptions.')
]
