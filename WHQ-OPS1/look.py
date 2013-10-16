#!/usr/bin/python

import cgi
import cgitb
import pexpect
import sys
import socket
import re
from netaddr import *

cgitb.enable()

form = cgi.FieldStorage()
password = "IPStor101"

def engine(command, target):
    # 
    child = pexpect.spawn(target)
    child.expect('config')
    child.sendline (password)
    child.expect('config')
    child.sendline("set cli screen-length 0") 
    child.expect('config')
    child.sendline("set cli screen-width 0") 
    child.expect('config')
    child.sendline(command)
    child.expect('config@')
    output = child.before
    child.sendline('exit')
    return output

def main():
    target = '/usr/bin/ssh -o "StrictHostKeyChecking no" config@' + form.getvalue('router')
    command_dict = {"ospf" : "show ospf",
                    "route" : "show route",
                    "log" : "show log",
                    "arp" : "show arp",
                    "firewall": "show firewall",
                    "interface": "show interface",
                    "configuration": "show configuration",
                    "bgp": "show bgp",
                    "esw": "show ethernet-switching",
    }

    short  = command_dict[form.getvalue('command')]

    if form.getvalue('options'):
        command  = short + " " + form.getvalue('options')
    elif form.getvalue('command') == "route":
        print 'Content-type: text/html\r\n\r'
        print '<html>'
        print " Error 'show route' requires an option"
        return
    else:
        command = short

    output = engine(command, target)

    output_line_list = output.split('\r\n')

    print 'Content-type: text/html\r\n\r'
    print '<html>'
    print '<font face="courier" size="3">'
    for line in output_line_list:
        print line
        print "<br>"
    print "<br>"
    print "</font>"
    print '</html>'




main()