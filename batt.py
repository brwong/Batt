#!/usr/bin/python

##
## BATTERY STATUS BAR
## Parses and formats string output of the
## battery check program.
## Requires the acpi program (quits gracefully).
## Written by Brandon Wong; March 1, 2012.
##
## Prints a visual bar, percentage, and
## either time remaining (when unplugged)
## or a + (plus sign) (when charging).
##
## Script will take the last integer number as
## the length of the visual bar (in characters),
## and any non-number as a command to not
## print a trailing newline (useful for command
## prompt modification).
##

from os import popen
from sys import stdout, argv

l = 20 # length of the bar
linebreak = True
if len(argv) > 1:
	for arg in argv[1:]:
		try:
			int(arg)
		except:
			linebreak = False
		else:
			l = int(arg)

# run the battery check script
b = popen('acpi -b 2> /dev/null').read()
# if the script returns nothing
if b == '' or b.find('%')==-1:
	exit()

rem = ""
pos = b.find(' remaining')
if pos != -1:
	timerem = b[b.rfind(' ', 0, pos):pos].split(':')
	if len(timerem)==3:
		rem = 0
		rem += int(timerem[0]) * 60
		rem += int(timerem[1])
		rem = ' ' + str(rem) + " mins"
elif b.find(' until charged'):
	rem = "+"


try:
	p = int(b[b.rfind(' ', 0, b.find('%'))+1:b.find('%')]) # percentage
except:
	exit()
else:
	have = (l*p/100)
	donthave = l - have
	stdout.write(unichr(int('2592',16))*have + unichr(int('2591',16))*donthave + str(p).rjust(3) + '%' + rem)
	if linebreak:
		stdout.write('\n')


