toLoad  = ['hello', 'url', 'weather', 'help', 'roll']
plugins = __import__('lib.plugins', fromlist=toLoad)

class Message:
    def __init__(self):
        self.toLoad = toLoad
        return

    def reloadPlugins(self):
        plugins = None
        plugins = __import__('lib.plugins', fromlist=toLoad)
        for mod in toLoad:
            reload(getattr(plugins, mod))

    def process(self, channel, msg, source, irc, silent, config):
        self.channel = channel
        self.msg     = msg
        self.source  = source
        self.irc     = irc
        self.silent  = silent
        self.config  = config
        
        for mod in toLoad:
            try:
                getattr(plugins, mod).match(self)
            except:
                self.irc.msg(self.channel, mod + " plugin broken.")