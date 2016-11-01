from functools import wraps
import asyncio

def get_client_and_message(args) :
    if len(args) == 2 :
        return (args[0], args[1])
    else :
        return (args[1], args[2])

def only_owner_top_role(func) :
    """Only those who have the same top_role than the owner of the server are able to use the function."""
    @wraps(func)
    @asyncio.coroutine
    def wrapper(*args) :
        if len(args) == 2 :
            message = args[0]
            client = args[1]
        else :
            message = args[1]
            client = args[2]
        if message.server.owner.top_role in message.author.roles :
            yield from func(*args)
        else :
            yield from client.send_message(message.channel, "Vous n'êtes pas autorisé à exécuter cette commande...")
    return wrapper

def require_non_private(func) :
    """The function should work only for non private channels."""
    @wraps(func)
    @asyncio.coroutine
    def wrapper(*args) :
        message, client = get_client_and_message(args)
        if message.channel.is_private :
            yield from client.send_message(message.channel, "Cette commande ne peut pas être exécuté par message privé...")
        else :
            yield from func(*args)
    return wrapper
