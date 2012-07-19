import re
import urllib
import htmlentitydefs
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
                toSend =  htmlentitydecode(BeautifulSoup(title).__str__('utf-8').replace('\r', '').replace('\n', '').strip())
                
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

def htmlentitydecode(s):
    return re.sub('&(%s);' % '|'.join(name2codepoint), 
            lambda m: unichr(name2codepoint[m.group(1)]), s)

def unescape(s):
    s = s.replace("%20", " ")
    s = s.replace("%21", "!")
    s = s.replace("%22", "\"")
    s = s.replace("%23", "#")
    s = s.replace("%24", "$")
    s = s.replace("%25", "%")
    s = s.replace("%26", "&")
    s = s.replace("%27", "\'")
    s = s.replace("%28", "(")
    s = s.replace("%29", ")")
    s = s.replace("%2A", "*")
    s = s.replace("%2B", "+")
    s = s.replace("%2C", ",")
    s = s.replace("%2D", "-")
    s = s.replace("%2E", ".")
    s = s.replace("%2F", "/")
    return s