import urllib.request
import urllib.parse
import re

def getFirstResult(query) :
    query_string = urllib.parse.urlencode({"search_query" : query})
    html_content = urllib.request.urlopen("http://www.youtube.com/results?" + query_string)
    search_results = re.findall(r'href=\"\/watch\?v=(.{11})', html_content.read().decode())
    if len(search_results) > 0 :
        return 'http://www.youtube.com/watch?v=' + search_results[0]
    else :
        return None
