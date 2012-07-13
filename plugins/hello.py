def match(msg):
    if msg.msg == "hello" and msg.silent:
        msg.irc.msg(msg.channel, "yo " + msg.source)
