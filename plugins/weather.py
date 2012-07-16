import re
import urllib
from   BeautifulSoup import BeautifulStoneSoup, BeautifulSoup

wxMatch = re.compile('\!w (\d{5})', flags=re.IGNORECASE)

def match(msg):
    for match in wxMatch.findall(msg.msg):
       if msg.silent:
           url     = 'http://rss.accuweather.com/rss/liveweather_rss.asp?metric=0&locCode=' + match
           httpreq = urllib.urlopen(url)
           doc     = BeautifulStoneSoup(httpreq)
           weather = BeautifulSoup(doc.findAll('description')[2].contents[0]).__str__('utf-8').replace('\r', '').replace('\n', '').replace(' &#176;', '').split('&lt;')[0]
           msg.irc.msg(msg.channel, msg.source + ': ' + weather )
