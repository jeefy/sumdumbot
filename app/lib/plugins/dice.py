"""
Roll dem dice
"""
import re
import random

helloMatch = re.compile('\!roll\s*(\d*)')

def match(msg):
	roll = helloMatch.match(msg.msg)
	if roll is not None and msg.silent:
		try:
			sides = int(roll.group(1))
		except:
			sides = 20
		msg.irc.msg(msg.channel, msg.source + " rolled a " + str(random.randint(1,sides)))
