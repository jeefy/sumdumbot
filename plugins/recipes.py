import re
import urllib
import random
from   BeautifulSoup import BeautifulStoneSoup, BeautifulSoup

def match(msg):
    parts = msg.msg.split(' ', 1)
    if parts[0] == "!recipe" and len(parts)>1:
        if msg.silent:
            url     = 'http://allrecipes.com/search/default.aspx?qt=k&sb=ra&wt=' + parts[1]
            httpreq = urllib.urlopen(url)
            doc     = BeautifulSoup(httpreq)
            results = doc.findAll("h3", {"class" : "resultTitle"})
            count   = len(results)
            key     = random.randint(0,count-1)
            tag     = BeautifulSoup(results[key].contents[1].string)
            msg.irc.msg(msg.channel, msg.source + ': [' + str(results[key].contents[1].string) + '] ' + str(results[key].contents[1]['href']) )
            args = {'title': str(results[key].contents[1].string), 'user': msg.source, 'url': str(results[key].contents[1]['href']), 'channel': msg.channel}
            response = urllib.urlopen('http://otakushirts.com/link/add?' + urllib.urlencode(args))

    if parts[0] == "!recipe" and len(parts) == 1:
        msg.irc.msg(msg.channel, msg.source + ': Improper use of command. (ex. !recipe mexican)')
