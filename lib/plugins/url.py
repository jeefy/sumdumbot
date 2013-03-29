import re
import urllib2
import urllib
import htmlentitydefs
from BeautifulSoup import BeautifulSoup
from BeautifulSoup import BeautifulStoneSoup

urlMatch = re.compile('(https?\:\/\/[^\s]+)', flags=re.IGNORECASE)

def match(msg):
    for match in urlMatch.findall(msg.msg):
        toSend  = ""
        try:
             httpreq = urllib2.urlopen(match)
             info    =  httpreq.info()
        except urllib2.HTTPError, x:
             return False 
        if info['Content-Type'].find('text/html') != -1:
            htmlBody = BeautifulSoup(httpreq)
#            title   = htmlBody.html.head.title.string
            try:
                title = htmlBody.findAll('title')[0].text
            except:
                title = None
            if title is not None:
                toSend =  BeautifulSoup(title).__str__('utf-8').replace('\r', '').replace('\n', '').strip()
#                toSend =  BeautifulStoneSoup(toSend,convertEntities=BeautifulStoneSoup.HTML_ENTITIES).contents[0]
            else:
                toSend = "No Title Found"
        else:
            toSend = "Binary Data or File"

        if msg.silent:
            msg.irc.msg(msg.channel, "[ " + toSend + " ]")
        
        args = {'title': toSend, 'user': msg.source, 'url': match, 'channel': msg.channel}
        response = urllib.urlopen('http://otakushirts.com/link/add?' + urllib.urlencode(args))
        if response.read() != "OK" and msg.silent:
            msg.irc.msg(msg.channel, "Error adding link to archive!")
