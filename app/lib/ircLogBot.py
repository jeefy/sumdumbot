# twisted imports
from twisted.words.protocols import irc
from twisted.internet        import reactor, protocol
from twisted.python          import log
from twisted.internet        import task
# system imports
import time, sys, os
import json as simplejson

# custom imports
toLoad  = ["message"]#, "externalMessage"]
modules = {}
config  = __import__('data.config', fromlist=['config']).config

class SumDumBot(irc.IRCClient):
    nickname = config['irc']['nick']
    
    def connectionMade(self):
        for n in toLoad:
            modules[n] = __import__('lib.' + n, fromlist=[n])
        irc.IRCClient.connectionMade(self)

    def connectionLost(self, reason):
        irc.IRCClient.connectionLost(self, reason)

    def signedOn(self):
        for n in self.factory.channels:
            self.join(str(n))

    def joined(self, channel):
        return
    
    def _writeChannels(self):
        f = open(os.path.realpath(__file__).replace('/lib/ircLogBot.py', '/data/channels.conf'), 'w')
        f.write(simplejson.dumps(self.factory.channels))

    def privmsg(self, user, channel, msg):
        user = user.split('!', 1)[0]
        if self.factory.channels.has_key(channel[1:]):
            mesg = modules['message'].Message()
            mesg.process(channel, msg, user, self, self.factory.channels[channel[1:]], config)

    def action(self, user, channel, msg):
        user = user.split('!', 1)[0]

    def irc_NICK(self, prefix, params):
        old_nick = prefix.split('!')[0]
        new_nick = params[0]

    def alterCollidedNick(self, nickname):
        return nickname + '_'

class SumDumFactory(protocol.ClientFactory):
    def __init__(self):
        self.bot      = None
        self.channels = {}
        self.msgDB    = None
        self.home     = config['irc']['home']
        try:
            with open(os.path.realpath(__file__).replace('/lib/ircLogBot.py', '/data/channels.conf'), 'r') as f:
                self.channels = simplejson.loads(f.read())
        except IOError:
            with open(os.path.realpath(__file__).replace('/lib/ircLogBot.py', '/data/channels.conf'), 'w') as f:
                self.channels = {self.home: True}
                f.write(simplejson.dumps(self.channels))

    def buildProtocol(self, addr):
        p = SumDumBot()
        self.bot   = p
        p.factory  = self
        return p

    def clientConnectionLost(self, connector, reason):
        connector.connect()

    def clientConnectionFailed(self, connector, reason):
        print "connection failed:", reason
        reactor.stop()

#    def externalMessages(self):
#        if self.bot is not None:
#            msgDB = modules['externalMessage'].ExternalMessage(self, config)
#            msgDB.check()
