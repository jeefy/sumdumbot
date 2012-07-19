import re
import urllib
import htmlentitydefs
from htmlentitydefs import name2codepoint
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
                toSend =  decodeEntities(BeautifulSoup(title).__str__('utf-8').replace('\r', '').replace('\n', '').strip())
                
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

EntityPattern = re.compile('&(?:#(\d+)|(?:#x([\da-fA-F]+))|([a-zA-Z]+));')
def decodeEntities(s, encoding='utf-8'):
    def unescape(match):
        code = match.group(1)
        if code:
            return unichr(int(code, 10))
        else:
            code = match.group(2)
            if code:
                return unichr(int(code, 16))
            else:
                code = match.group(3)
                if code in name2codepoint:
                    return unichr(name2codepoint[code])
        return match.group(0)

    if isinstance(s, str):
        s = s.decode(encoding)
    return EntityPattern.sub(unescape, s)
