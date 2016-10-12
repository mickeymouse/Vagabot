from html.parser import HTMLParser
from html import unescape, escape

class CharacterParser(HTMLParser) :
    def __init__(self) :
        super(CharacterParser, self).__init__()
        self.classVal = ''
        self.race = ''
        self.sousRace = ''
        self.jobImg = ''
        self.title = ''
        self.img = ''
    
    def handle_starttag(self, tag, attrs) :
        if ('class', 'chara_profile_title') in attrs:
            self.classVal = 'chara_profile_title'
        if ('id', 'class_info') in attrs :
            self.classVal = 'class_info'
        if self.classVal == 'class_info' and ('class', 'ic_class_wh24_box') in attrs :
            self.classVal = 'job_info' #we want the job img
        if tag == 'img' :
            if self.classVal == 'job_info' :
                for (attr,val) in attrs :
                    if attr == 'src' :
                        self.jobImg = val
                        self.classVal = ''
                        break
            elif self.classVal == 'img_area' :
                for (attr,val) in attrs :
                    if attr == 'src' :
                        self.img = val
                        self.classVal = ''
                        break
        if ('class', 'chara_title') in attrs :
            self.classVal = 'chara_title'
        if ('class', 'img_area bg_chara_264') in attrs :
            self.classVal = 'img_area'
    
    def handle_data(self, data) :
        if self.classVal == 'miqote' :
            tmp = data.split(' / ')
            self.sousRace = tmp[1]
            self.classVal = ''
        elif self.classVal == 'chara_profile_title' :
            if not data.startswith('Miqo') :
                tmp = data.split(' / ')
                self.race = tmp[0]
                self.sousRace = tmp[1]
                self.classVal = ''
            else :
                self.race = 'Miqo\'te'
                self.classVal = 'miqote' #à cause de l'apostrophe le parser se stop -.-
        elif self.classVal == 'chara_title' :
            if len(self.title) > 0 :
                self.title += '\'' + data
            else :
                self.title = data

    def handle_endtag(self, tag) :
        if self.classVal == 'chara_title' :
            self.classVal = ''
