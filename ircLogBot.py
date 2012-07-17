# twisted imports
from twisted.words.protocols import irc
from twisted.internet import reactor, protocol
from twisted.python import log

# system imports
import time, sys, re
import simplejson
# custom imports
toLoad  = ["message"]
modules = {}

regex = {
    'join'  : re.compile('\: join #?(\w+)', flags=re.IGNORECASE),
    'leave' : re.compile('\: leave #?(\w+)', flags=re.IGNORECASE)
}


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

        elif user=="jeefy" and regex['join'].search(msg):
            newChan = msg.split(': ')[1].split(' ')
            silent = False
            if len(newChan) > 2 and newChan[2]=="true":
                silent = True
            self.factory.channels[newChan[1]] = silent
            self.join(newChan[1])
            f = open('channels.conf', 'a')
            f.write(simplejson.dumps({'channel':newChan[1], 'silent': silent})) 

        elif user=="jeefy" and regex['leave'].search(msg):
            newChan = msg.split(': ')[1].split(' ')
            silent = False
            if len(newChan) > 2 and newChan[2]=="true":
                silent = True
            self.factory.channels[newChan[1]] = silent
            self.leave(newChan[1])

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
        self.channels = {}
        f = open('channels.conf')
        for l in f.readlines():
            tmp = simplejson.loads(l)
            self.channels[tmp['channel']] = tmp['silent']

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
