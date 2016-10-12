import discord
import asyncio
import pickle
from KupoParser import parser as KParser
from Bot.player import Player
from Bot.poll import Poll

@asyncio.coroutine
def say(message, client) :
    arg = message.content.split()
    arg.pop(0)
    arg = ' '.join(arg)
    if arg != '' :
        yield from client.send_message(message.channel, arg)
    else :
        yield from client.send_message(message.channel, 'Utilisation !dire\/!say <message>')

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
def printHelp(message, client) :
    msg = 'Mes commandes sont les suivantes :\n'
    for (commandNames, handler, desc) in commandList :
        msg += commandNames + ' : ' + desc + '\n'
    yield from client.send_message(message.author, msg)
    
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
    ('!help', printHelp, 'Affiche la liste des commandes ainsi que leurs descriptions.')
]
