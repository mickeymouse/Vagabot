from html.parser import HTMLParser

class CreateCharacterParser(HTMLParser) :
    def __init__(self) :
        super(CreateCharacterParser, self).__init__()
        self.flag = False
        self.state = False
    
    def handle_starttag(self, tag, attrs) :
        if ('class', 'news__detail__wrapper') in attrs :
            self.flag = True

    def handle_data(self, data) :
        if self.flag :
            print(data)
            self.state = ('\\n\\xe3\\x80\\x80\\xe2\\x97\\x8b Moogle' in data)
            #self.reset()
