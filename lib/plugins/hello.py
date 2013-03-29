"""
Basic 
"""
import re

helloMatch = re.compile('hello friend', flags=re.IGNORECASE)

def match(msg):
    if helloMatch.match(msg.msg) and msg.silent:
        msg.irc.msg(msg.channel, "yo " + msg.source)
