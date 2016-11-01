import discord
import asyncio
from time import time
from Decorators import authorized

class Poll :
    def __init__(self) :
        self.delay = 7200 #time the opinion poll will last
        self.questions = dict() #the questions that are asked, each key must be a server
        self.answers = dict() #a dictionnary that store the vote of the users, each user can change his opinion but only the last is taken
        self.flags = dict() #a dictionnary of flags if turned to false the poll is terminated by force

    @authorized.require_non_private
    @asyncio.coroutine
    def yes(self, message, client) :
        if message.server not in self.questions :
            yield from client.send_message(message.channel, 'Il n\'y a aucun sondage en cours...')
        else :
            if message.author in self.answers[message.server] : #the author wants to change his vote
                yield from client.send_message(message.channel, 'Vote modifié !')
            else :
                yield from client.send_message(message.channel, 'Le vote a été pris en compte !')
            self.answers[message.server][message.author] = True

    @authorized.require_non_private
    @asyncio.coroutine
    def no(self, message, client) :
        if message.server not in self.questions :
            yield from client.send_message(message.channel, 'Il n\'y a aucun sondage en cours...')
        else :
            if message.author in self.answers[message.server] : #the author wants to change his vote
                yield from client.send_message(message.channel, 'Vote modifié !')
            else :
                yield from client.send_message(message.channel, 'Le vote a été pris en compte !')
            self.answers[message.server][message.author] = False

    @authorized.require_non_private
    @authorized.only_owner_top_role
    @asyncio.coroutine
    def abort(self, message, client) :
        if message.server in self.flags :
            self.flags[message.server] = False
            yield from client.send_message(message.channel, "Le sondage a été arrêté par un modérateur.")
        else :
            yield from client.send_message(message.channel, "Il n'y a aucun sondage en cours...")

    @authorized.require_non_private
    @asyncio.coroutine
    def setPoll(self, message, client) :
        """Set a new poll if none is set and show the results once the poll is over."""
        question = message.content.split()
        question.pop(0)
        question = ' '.join(question)
        if question != '' :
            if message.server in self.questions :
                yield from client.send_message(message.channel, 'Un sondage est déjà en cours, veuillez attendre qu\'il soit terminé...')
            else :
                self.questions[message.server] = question
                self.answers[message.server] = dict()
                yield from client.send_message(message.channel, 'Sondage en cours : ' + question)
                start = time()
                self.flags[message.server] = True
                while self.flags[message.server] and time() - start <= self.delay :
                    yield from asyncio.sleep(1) #we wait until the opinion poll is over and then show the result
                yes = 0
                answers = self.answers.pop(message.server)
                self.questions.pop(message.server)
                self.flags.pop(message.server)
                npoller = len(answers)
                if npoller == 0 :
                    yield from client.send_message(message.channel, 'Aucune personne n\'a voté...')
                    return None
                for k in answers :
                    if answers[k] :
                        yes+=1
                yes /= npoller
                yes *= 100
                s = 'Pour la question : '+ question + '\nSur un ensemble de {:d} personnes : '.format(npoller)
                if yes > 50 : #yes win
                    yield from client.send_message(message.channel, s + 'le oui l\'emporte avec {:.2f}% des votes.'.format(yes))
                elif yes < 50 :
                    yield from client.send_message(message.channel, s + 'le non l\'emporte avec {:.2f}% des votes.'.format(100-yes))
                else :
                    yield from client.send_message(message.channel, s + 'ni le oui ni le non l\'emporte.')
        else :
            if message.server in self.questions :
                yield from client.send_message(message.channel, 'Sondage en cours : '+ self.questions[message.server])
            else :
                yield from client.send_message(message.channel, 'Il n\'y a aucun sondage en cours...')
