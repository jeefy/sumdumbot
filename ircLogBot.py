# twisted imports
from twisted.words.protocols import irc
from twisted.internet import reactor, protocol
from twisted.python import log

# system imports
import time, sys, re
import simplejson
import git

# custom imports
toLoad  = ["message"]
modules = {}
config  = __import__('config', fromlist=['config']).config

regex = {
    'join'   : re.compile('\: join #?(\w+)', flags=re.IGNORECASE),
    'leave'  : re.compile('\: leave #?(\w+)', flags=re.IGNORECASE),
    'mute'   : re.compile('\: mute #?(\w+)', flags=re.IGNORECASE),
    'unmute' : re.compile('\: unmute #?(\w+)', flags=re.IGNORECASE)
}


class SumDumBot(irc.IRCClient):
    nickname = config['irc']['nick']

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
    
    def _writeChannels(self):
        f = open('channels.conf', 'w')
        f.write(simplejson.dumps(self.factory.channels))

    def privmsg(self, user, channel, msg):
        user = user.split('!', 1)[0]
        if user in config['admins'] and msg==self.nickname+": reload":
            self.msg(channel, "Reloading modules...")
            for n in toLoad:
                 reload(modules[n])
            mesg = modules['message'].Message()
            mesg.reloadPlugins()
            self.msg(channel, "Reloading complete")

        elif user in config['admins'] and msg==self.nickname+": gitpull":
            self.msg(channel, "Pulling from Github...")
            # Doin thangs
            repo = git.Repo('/home/jeef/sumdumbot')
            repo.remote().pull()
            for n in toLoad:
                 reload(modules[n])
            mesg = modules['message'].Message()
            mesg.reloadPlugins()
            self.msg(channel, "Pull / Reload complete!")

        elif user in config['admins'] and regex['join'].search(msg):
            newChan = msg.split(': ')[1].split(' ')
            silent = False
            if len(newChan) > 2 and newChan[2]=="true":
                silent = True
            self.factory.channels[newChan[1]] = silent
            self.join(newChan[1])
            self._writeChannels()

        elif user in config['admins'] and regex['leave'].search(msg):
            newChan = msg.split(': ')[1].split(' ')
            self.leave(newChan[1])
            self._writeChannels()
        
        elif user in config['admins'] and regex['mute'].search(msg):
            newChan = msg.split(': ')[1].split(' ')
            self.factory.channels[newChan[1]] = False
            self.msg(channel, newChan[1] + ' now muted')
            self._writeChannels()

        elif user in config['admins'] and regex['unmute'].search(msg):
            newChan = msg.split(': ')[1].split(' ')
            self.factory.channels[newChan[1]] = True
            self.msg(channel, newChan[1] + ' now unmuted')
            self._writeChannels()

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
        self.channels = simplejson.loads(f.read())

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
    reactor.connectTCP(config['irc']['server'], config['irc']['port'], f)

    # run bot
    reactor.run()
