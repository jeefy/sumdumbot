def match(msg):
    if msg.msg == "!help" and msg.silent:
        msg.irc.msg(msg.source, "Hello friend! I'm capable of the following commands and functions: ")
        msg.irc.msg(msg.source, "!w ZIPCODE for current weather (ex !w 48103) ")
        msg.irc.msg(msg.source, "!wd ZIPCODE for current and future weather (ex !wd 48103) ")
        msg.irc.msg(msg.source, "!recipe SEARCH for a random top 20 recipe from allrecipes.com (ex !recipe mexican) ")

        msg.irc.msg(msg.source, "-------- ")
        msg.irc.msg(msg.source, "Any link posted is archived and added to http://otakushirts.com ")
        msg.irc.msg(msg.source, "-------- ")
        msg.irc.msg(msg.source, "Direct any questions you may have to my creator, jeefy ")
