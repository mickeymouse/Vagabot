from KupoParser.configs import Configs
from html.parser import HTMLParser

def littleStrip(word) :
    newWord = ''
    i = 0
    while (i < len(word) and word[i] == '\\') :
        i += 2
    while ( i < len(word) and word[i] != '\\') :
        newWord += word[i]
        i += 1
    return newWord    

class WorldParser(HTMLParser) :
    """ This class has for purpose to parse the informations from
        the world status webpage and get the status of the world in the
        configs file """
    def __init__(self) :
        super(WorldParser, self).__init__()
        self.state = False
        self.flag = False
        self.dataWanted = False
    
    def handle_starttag(self, tag, attrs) :
        if ( ('class', 'worldstatus_1') in attrs ) :
            self.flag = True
        if ( self.flag and ('class', 'relative') in attrs ) :
            self.dataWanted = True
        if ( self.flag and ('class', 'ic_worldstatus_1') in attrs ) :
            self.dataWanted = True
            self.flag = False
    
    def handle_data(self, data) :
        if self.flag and self.dataWanted :
            flag = (littleStrip(data) == Configs['world'])
            self.dataWanted = False
        if not self.flag and self.dataWanted :
            self.state = (littleStrip(data) == 'En service')
            self.dataWanted = False
            self.reset()
