# twisted imports
from twisted.words.protocols import irc
from twisted.internet import reactor, protocol
from twisted.python import log

# system imports
import time, sys

# custom imports
toLoad  = ["message"]
modules = {}

class SumDumBot(irc.IRCClient):
    nickname = "onedumbot"

    def connectionMade(self):
        for n in toLoad:
            modules[n] = __import__(n)
        irc.IRCClient.connectionMade(self)

    def connectionLost(self, reason):
        irc.IRCClient.connectionLost(self, reason)

    def signedOn(self):
        for n in self.factory.channels:
            self.join(n)

    def joined(self, channel):
	return

    def privmsg(self, user, channel, msg):
        user = user.split('!', 1)[0]
        if user=="jeefy" and msg==self.nickname+": reload":
            self.msg(channel, "Reloading modules...")
            for n in toLoad:
                 reload(modules[n])
            mesg = modules['message'].Message()
            mesg.reloadPlugins()
            self.msg(channel, "Reloading complete")
        elif self.factory.channels.has_key(channel[1:]):
            mesg = modules['message'].Message()
            
            mesg.process(channel, msg, user, self, self.factory.channels[channel[1:]])

    def action(self, user, channel, msg):
        user = user.split('!', 1)[0]

    def irc_NICK(self, prefix, params):
        """Called when an IRC user changes their nickname."""
        old_nick = prefix.split('!')[0]
        new_nick = params[0]

    def alterCollidedNick(self, nickname):
        return nickname + '_'

class SumDumFactory(protocol.ClientFactory):
    def __init__(self):
        self.channels = {
            'otakushirts': False,
            'onedumbot':   True,
        }

    def buildProtocol(self, addr):
        p = SumDumBot()
        p.factory = self
        return p

    def clientConnectionLost(self, connector, reason):
        """If we get disconnected, reconnect to server."""
        connector.connect()

    def clientConnectionFailed(self, connector, reason):
        print "connection failed:", reason
        reactor.stop()


if __name__ == '__main__':
    # create factory protocol and application
    f = SumDumFactory()

    # connect factory to this host and port
    reactor.connectTCP("irc.freenode.net", 6667, f)

    # run bot
    reactor.run()
