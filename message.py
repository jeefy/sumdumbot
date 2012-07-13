import re

toLoad  = ['hello', 'url']
plugins = __import__('plugins', fromlist=toLoad)

class Message:
    def __init__(self):
        return

    def reloadPlugins(self):
        plugins = None
        plugins = __import__('plugins', fromlist=toLoad)
        for mod in toLoad:
            reload(getattr(plugins, mod))

    def process(self, channel, msg, source, irc, silent):
        self.channel = channel
        self.msg     = msg
        self.source  = source
        self.irc     = irc
        self.silent  = silent
        
        for mod in toLoad:
            getattr(plugins, mod).match(self)
        #match message against regexs
	return
