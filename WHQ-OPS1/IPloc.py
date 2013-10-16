#!/usr/bin/python
"""
Written by:     Joseph Goldberg
Created:        May 4, 2013
Last Updated:   May 20, 2013
Version:        0.01  Basic Application that finds locations based on MAC or IP Address
Version:        0.02  Add basic layer 2 pathing

"""


import cgi
import cgitb
import pexpect
import sys
import socket
import re
from netaddr import *

cgitb.enable()


# Global Variables
core_router = "172.16.2.30"
wc_dist_sw = "172.16.9.51"
ec_dist_sw = "172.16.9.31"
password = "IPStor101"
search_for = ""
IP_address = ""
MAC_address = ""
jack_num = ""
form = cgi.FieldStorage()
wc_uplink = []
ec_uplink = []
sw_hops = []
mac_man = ""

#  *** Don't Edit Below This Point ***

# Class definations
class mac_custom(mac_unix): pass
# Custom MAC conversion for UNIX with leading 0
mac_custom.word_fmt = '%.2X'

def is_valid_ipv4_address(address):
    # Test that user entered IPv4 Address is valid
    try:
        addr= socket.inet_pton(socket.AF_INET, address)
    except AttributeError: # no inet_pton here, sorry
        try:
            addr= socket.inet_aton(address)
        except socket.error:
            return False
        return address.count('.') == 3
    except socket.error: # not a valid address
        return False

    return True

def is_valid_ipv6_address(address):
    # Test that user entered IPv6 Address is valid
    try:
        addr= socket.inet_pton(socket.AF_INET6, address)
    except socket.error: # not a valid address
        return False
    return True

def mac_maker():
    global mac_man
    mac = EUI(MAC_address)
    oui = mac.oui
    mac_man = oui.registration().org

def is_valid_MAC(address):
    # Regex to test if MAC Address is valid
    global MAC_address, mac_man
    if re.match("[0-9a-f]{2}([:])[0-9a-f]{2}(\\1[0-9a-f]{2}){4}$", address.lower()):
        temp = EUI(address, dialect=mac_custom)
        mac_maker()
        MAC_address = str(temp).lower()
        return True
    elif re.match("[0-9a-f]{2}([-])[0-9a-f]{2}(\\1[0-9a-f]{2}){4}$", address.lower()):
        temp = EUI(address, dialect=mac_custom)
        mac_maker()
        MAC_address = str(temp).lower()
        return True
    else:
        return False

def get_core_router(command, target):
    # Get the IP / MAC info from the core router
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
    arp = child.before
    child.sendline('exit')

    return arp.split()

def search_address(match):
    # if the user entered an IP address to search for, this is the search engine
    global jack_num
    found = False
    mac = match[6]
    command = "show ethernet-switching table | match " + mac
    target = '/usr/bin/ssh -o "StrictHostKeyChecking no" config@' + wc_dist_sw
    wc_return = get_core_router (command, target)
    sw_hops.append([wc_return[0][1:-1], wc_return[11][:-2]])
    
    # test for matches in the EC and WC config files from the dist switches
    # West Closet Tests
    for x in wc_uplink:
        test = x.split()
        if test[0] == wc_return[-1]:
            dest_switch = test[1]
            if dest_switch != "falc-ecfl2-01" and dest_switch != "FALC-ECFL2-01":
                found = True
   
    # If not in the west closet then check the east closet
    if found == False:
        target = '/usr/bin/ssh -o "StrictHostKeyChecking no" config@' + ec_dist_sw
        ec_return = get_core_router (command, target)
        sw_hops.append([ec_return[0][1:-1], ec_return[11][:-2]])
        
        for x in ec_uplink:
            test = x.split()
            if test[0] == ec_return[-1]:
                dest_switch = test[1]
                found = True

    # If we found an IP in the table then continue search otherwise error out cleanly
    if found == True:
        target = '/usr/bin/ssh -o "StrictHostKeyChecking no" config@' + dest_switch
        edge_switch_return = get_core_router (command, target)

        # account for no description on .0 sub-interface so strip it
        dest_port = edge_switch_return[-1][:-2]

        command = 'show interfaces descriptions ' + dest_port

        final = get_core_router (command, target)
        sw_hops.append([final[0][1:-1], dest_port])

        jack_num = final[-1]
    else:
        # IP was not currently in the table
        print 'Content-type: text/html\r\n\r'
        print '<html>'
        print "Address Not in Table"
        print "<br>"
        print '</html>'

def display_results():
        print 'Content-type: text/html\r\n\r'
        print '<html>'  
        print '<p><img height="110" src="/netglobe.png" width="110"/><img height="90" src="/falconstor.png" width="250"/></p>'
        print '<h1>Search Results</h1>'
        print '<table style>'
        print '<tr>'
        print '   <td width="200px"><b>IP Address:</b></td>'
        print '   <td width="500px"><b>%s</b>&nbsp;</td>' % IP_address
        print '</tr>'
        print '<tr>'
        print '    <td width="200px"><b>MAC Address:</b></td>'
        print '    <td width="500px"><b>%s</b></td>' % MAC_address
        print '</tr>'
        print '<tr>'
        print '    <td width="200px"><b>Manufacturer:</b></td>'
        print '    <td width="500px"><b>%s</b></td>' % mac_man
        print '</tr>'        
        print '<tr>'
        print '    <td width="200px"><b>Jack Number:</b></td>'
        print '    <td width="500px"><b>%s</b></td>' % jack_num
        print '</tr>'
        print '</table>' 
        print '<table>'
        print '<br>'
        print '<br>'
        print '<H2>Layer 2 Path Diagram</H2>'

        for x in sw_hops:
            print '<tr>'
            print '   <td width="100px">'
            print '   <img height="50" src="/switch.png" width="70"/> </td>'
            print '   <td width="200px">Switch: %s <br> Port:   %s</td>' % (x[0], x[1])
            print '</tr>'
            print '<tr>'
            print '   <td width="100px" align="center">'
            print '   <img height="70" src="/downarrow.png" width="40"/> </td>'
            print '   <td width="200px" align="center">'
            print '   <img height="70" src="/downarrow.png" width="40"/> </td>'
            print '</tr>'
        print '<tr>'
        print '   <td width="100px">'
        print '   <img height="60" src="/jack.png" width="80"/> </td>'
        print '   <td width="200px">Jack Number: %s</td>' % (jack_num)
        print '</table>'

        print '</html>'


def get_result(command, target):
    # Core Functionality
    global IP_address, MAC_address, jack_num
    match = get_core_router(command, target)
    
    if search_for == "IP":
        MAC_address = match[6]
        mac_maker()
        final = search_address(match)
        display_results()

    if search_for == "MAC":
        IP_address = match[7]
        final  = search_address(match)
        display_results()

def main():
    # Process the form
    global search_for, IP_address, MAC_address, jack_num, wc_uplink, ec_uplink, sw_hops

    # Open and process closet config files
    wc_file = open("west_closet.cfg", "r")
    ec_file = open("east_closet.cfg", "r")

    for line in wc_file:
        wc_uplink.append(line)

    for line in ec_file:
        ec_uplink.append(line)


    if form.getvalue('searchtype') == "IP" and form.getvalue('search'):
        IP_address = form.getvalue('search')
        
        # Test if IP address is valid
        if is_valid_ipv4_address(IP_address) == True:
            command = "show arp | match " + IP_address
            target = '/usr/bin/ssh -o "StrictHostKeyChecking no" config@' + core_router
            search_for = "IP"
            get_result(command, target)
        else:
            print 'Content-type: text/html\r\n\r'
            print '<html>'
            print "Invalid IP Address"
            print "<br>"
            print '</html>'
    elif form.getvalue('searchtype') == "MAC" and form.getvalue('search'):
        MAC_address = form.getvalue('search').lower()

        if is_valid_MAC(MAC_address) == True:
            target = '/usr/bin/ssh -o "StrictHostKeyChecking no" config@' + core_router
            command = "show arp | match " + MAC_address
            search_for = "MAC"
            get_result(command, target)
        else:
            print 'Content-type: text/html\r\n\r'
            print '<html>'
            print "Invalid MAC Address"
            print "<br>"
            print '</html>' 
    elif form.getvalue('searchtype') == "jack" and form.getvalue('search'):
        jack_num = form.getvalue('search')
        search_for = "location"
        print 'Content-type: text/html\r\n\r'
        print '<html>'
        print jack_num
        print "<br>"
        print '</html>'
    else:
        print 'Content-type: text/html\r\n\r'
        print '<html>'
        print "Error, you must fill in at least one form"
        print form.getvalue('MAC_address')
        print "<br>"
        print '</html>'


main()
