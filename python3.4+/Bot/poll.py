import discord
import asyncio

class Poll :
    def __init__(self) :
        self.delay = 7200 #time the opinion poll will last
        self.question = '' #the question that is asked '' if none
        self.answers = dict() #a dictionnary that store the vote of the users, each user can change his opinion but only the last is taken

    @asyncio.coroutine
    def yes(self, message, client) :
        if self.question == '' :
            yield from client.send_message(message.channel, 'Il n\'y a aucun sondage en cours...')
        else :
            if message.author in self.answers : #the author want to change his vote
                yield from client.send_message(message.channel, 'Vote modifié !')
            else :
                yield from client.send_message(message.channel, 'Le vote a été pris en compte !')
            self.answers[message.author] = True

    @asyncio.coroutine
    def no(self, message, client) :
        if self.question == '' :
            yield from client.send_message(message.channel, 'Il n\'y a aucun sondage en cours...')
        else :
            if message.author in self.answers : #the author want to change his vote
                yield from client.send_message(message.channel, 'Vote modifié !')
            else :
                yield from client.send_message(message.channel, 'Le vote a été pris en compte !')
            self.answers[message.author] = False

    @asyncio.coroutine
    def setPoll(self, message, client) :
        """Set a new poll if none is set and show the results once the poll is over."""
        question = message.content.split()
        question.pop(0)
        question = ' '.join(question)
        if question != '' :
            if self.question != '' :
                yield from client.send_message(message.channel, 'Un sondage est déjà en cours, veuillez attendre qu\'il soit terminé...')
            else :
                self.question = question
                yield from client.send_message(message.channel, 'Sondage en cours : ' + self.question)
                yield from asyncio.sleep(self.delay) #we wait until the opinion poll is over and then show the result
                yes = 0
                npoller = len(self.answers)
                if npoller == 0 :
                    yield from client.send_message(message.channel, 'Aucune personne n\'a voté...')
                    self.question = ''
                    return None
                for k in self.answers :
                    if self.answers[k] :
                        yes+=1
                yes /= npoller
                yes *= 100
                s = 'Pour la question : '+ self.question + '\nSur un ensemble de {:d} personnes : '.format(npoller)
                if yes > 50 : #yes win
                    yield from client.send_message(message.channel, s + 'le oui l\'emporte avec {:.2f}% des votes.'.format(yes))
                elif yes < 50 :
                    yield from client.send_message(message.channel, s + 'le non l\'emporte avec {:.2f}% des votes.'.format(100-yes))
                else :
                    yield from client.send_message(message.channel, s + 'ni le oui ni le non l\'emporte.')
                self.question = ''
                self.answers.clear()
        else :
            if self.question != '' :
                yield from client.send_message(message.channel, 'Sondage en cours : '+ self.question)
            else :
                yield from client.send_message(message.channel, 'Il n\'y a aucun sondage en cours...')
