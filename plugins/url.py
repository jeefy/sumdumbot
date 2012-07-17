import re
import urllib
from BeautifulSoup import BeautifulSoup

urlMatch = re.compile('(https?\:\/\/[^\s]+)', flags=re.IGNORECASE)

def match(msg):
    for match in urlMatch.findall(msg.msg):
        toSend  = ""
        httpreq = urllib.urlopen(match)
        info    =  httpreq.info()
        if info['Content-Type'].find('text/html') != -1:
            title   = BeautifulSoup(httpreq).title.string
            if title is not None:
                toSend =  BeautifulSoup(title).__str__('utf-8').replace('\r', '').replace('\n', '').strip() 
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
