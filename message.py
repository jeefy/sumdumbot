import re

class Message:
    def __init__(self, channel, msg, source, irc):
        self.channel = channel
	self.msg     = msg
	self.source  = source
	self.irc     = irc

        irc.msg(channel, msg)

        return
    def process(self):
        #match message against regexs
	return
