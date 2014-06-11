#!/usr/bin/python
from lib.ircLogBot import SumDumBot, SumDumFactory
from twisted.words.protocols import irc
from twisted.internet        import reactor, protocol
from twisted.python          import log
#from twisted.internet        import task

if __name__ == '__main__':
    # create factory protocol and application
    config  = __import__('data.config', fromlist=['config']).config
    f       = SumDumFactory()
    #m       = task.LoopingCall(f.externalMessages)
    
    #m.start(5.0)
    reactor.connectTCP(config['irc']['server'], config['irc']['port'], f)

    #And so it begins...
    try:
        reactor.run()
    except KeyboardInterrupt:
        reactor.stop()
        print "Clean exit"