regex = {
    'join'   : re.compile('\: join #?(\w+)', flags=re.IGNORECASE),
    'leave'  : re.compile('\: leave #?(\w+)', flags=re.IGNORECASE),
    'mute'   : re.compile('\: mute #?(\w+)', flags=re.IGNORECASE),
    'unmute' : re.compile('\: unmute #?(\w+)', flags=re.IGNORECASE)
}

def match(msg):
    if msg.source in msg.config['admins'] and msg=="!reload":
        msg.irc.msg(channel, "Reloading modules...")
        mesg.reloadPlugins()
        msg.irc.msg(channel, "Reloading complete")

    elif msg.source in msg.config['admins'] and msg=="!gitpull":
        msg.irc.msg(channel, "Pulling from Github...")
        # Doin thangs
        repo = git.Repo(msg.config['path'])
        repo.remote().pull()
        for n in toLoad:
             reload(modules[n])
        msg.reloadPlugins()
        msg.irc.msg(channel, "Pull / Reload complete!")

    elif msg.source in msg.config['admins'] and regex['join'].search(msg):
        newChan = msg.split(': ')[1].split(' ')
        silent = False
        if len(newChan) > 2 and newChan[2]=="true":
            silent = True
        msg.irc.factory.channels[newChan[1]] = silent
        msg.irc.join(newChan[1])
        msg.irc._writeChannels()

    elif msg.source in msg.config['admins'] and regex['leave'].search(msg):
        newChan = msg.split(': ')[1].split(' ')
        msg.irc.leave(newChan[1])
        msg.irc._writeChannels()
    
    elif msg.source in msg.config['admins'] and regex['mute'].search(msg):
        newChan = msg.split(': ')[1].split(' ')
        msg.irc.factory.channels[newChan[1]] = False
        msg.irc.msg(channel, newChan[1] + ' now muted')
        msg.irc._writeChannels()

    elif msg.source in msg.config['admins'] and regex['unmute'].search(msg):
        newChan = msg.split(': ')[1].split(' ')
        msg.irc.factory.channels[newChan[1]] = True
        msg.irc.msg(channel, newChan[1] + ' now unmuted')
        msg.irc._writeChannels()