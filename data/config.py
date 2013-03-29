import socket

config = {
    "owner"  : "jeefy",
    "admins" : ['jeefy', 'jeef', 'Oddykun'],
    "path"   : "/home/jeef/sumdumbot",
    "dbPath" : "/home/jeef/sumdumbot/data/messages.db",
    "irc"    : {
        "server": "irc.freenode.net",
        "port"  : 6667,
        "nick"  : "sumdumbot",
        "home"  : "#otakushirts"
    }
}

if socket.gethostname() != "archives":
    config['irc']['nick'] = "testbot_" + socket.gethostname()