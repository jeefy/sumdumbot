import socket, os

config = {
    "owner"  : "jeefy",
    "admins" : ['jeefy', 'jeef', 'Oddykun'],
    "path"   : os.path.realpath(__file__).replace('/lib/ircLogBot.py', '/'),
    #"dbPath" : os.path.realpath(__file__).replace('/lib/ircLogBot.py', '/data/messages.db'),
    "irc"    : {
        "server": "irc.freenode.net",
        "port"  : 8000,
        "nick"  : "sumdumbot",
        "home"  : "#otakushirts"
    }
}

if os.environ['TEST'] != "0":
    config['irc']['nick'] = "testbot_" + socket.gethostname()