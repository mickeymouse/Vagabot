from urllib.request import urlopen

from KupoParser.configs import Configs, jobImgs
from KupoParser.WorldParser import WorldParser
from KupoParser.CharacterParser import CharacterParser
from KupoParser.linkGetter import LinkGetter, CharacterGetter

def isWorldUp() :
    """return True if the world is up False otherwise"""
    parser = WorldParser()
    with urlopen(Configs['worldstatusURL']) as response :
        html = str(response.read()) #TODO c'est pas propre il vaudrait mieux faire un decode et retirer le littleStrip
    try :
        parser.feed(html)
    except Exception :
        pass
    return parser.state;
    
def isCharCreatable() :
    """return True if a character can be created in the world, False otherwise"""
    parser = LinkGetter('Concernant les restrictions de création de personnages')
    with urlopen(Configs['newsURL']) as response :
        html = response.read().decode()
    try :
        parser.feed(html)
    except Exception :
        pass
    with urlopen(Configs['ffxivURL']+parser.href) as response :
        html = str(response.read())
    return ('\\n\\xe3\\x80\\x80\\xe2\\x97\\x8b '+Configs['world']) in html

def registerCharIn(dic, query, author) :
    """register a new character given by the query in the dictionnary given in parameter dic, return True if everything is ok, False otherwise"""
    parser = CharacterGetter()
    with urlopen(Configs['charURL']+'?q='+query+'&worldname='+Configs['world']) as response :
        html = response.read().decode()
    try :
        parser.feed(html)
    except Exception :
        pass
    if parser.href != '' :
        dic[author] = (parser.href, ' '.join(query.split('+')))
        return True
    return False
    
def getCharacterInfo(characterURL, characterName) :
    """return a formatted string corresponding to the character information of the character given in parameter."""
    ans = '**'+characterName+'**'
    parser = CharacterParser()
    with urlopen(Configs['ffxivURL'] + characterURL) as response :
        html = response.read().decode()
    parser.feed(html)
    if (parser.title != '') :
        ans += ', *'+parser.title+'*'
    ans += '\n'+parser.race+', '+parser.sousRace+'\n'
    #ans += jobImgs[parser.jobImg]+'\n'
    ans += 'Page du personnage : '+ Configs['ffxivURL'] + characterURL + '\n\n'
    ans += parser.img
    return ans
        
def getGameUrl() :
    """return ffxiv website url"""
    return Configs['ffxivURL']
