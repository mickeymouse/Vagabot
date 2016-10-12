from html.parser import HTMLParser

class LinkGetter(HTMLParser) :
    def __init__(self, word) :
        super(LinkGetter, self).__init__()
        self.flag = False
        self.word = word
        self.href = ''
    
    def handle_starttag(self, tag, attrs) :
        if ('class', 'link') in attrs :
            self.flag = True
            for (attr, value) in attrs :
                if attr == 'href' :
                    self.href = value
                    break

    def handle_data(self, data) :
        if ( self.flag and (word in data) ) :
            self.reset()
        self.flag = False

class CharacterGetter(HTMLParser) :
    def __init__(self) :
        super(CharacterGetter, self).__init__()
        self.flag = False
        self.href = ''
    
    def handle_starttag(self, tag, attrs) :
        if ( tag == 'h4' and ('class', 'player_name_gold') in attrs ) :
            self.flag = True
        elif self.flag and tag == 'a' :
            self.href = attrs[0][1]
            self.reset()
