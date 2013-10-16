#!/usr/bin/python

import cgi
import cgitb
cgitb.enable()

print "Content-Type: text/html"     # HTML is following
print                               # blank line, end of headers

print "<TITLE>CGI script output</TITLE>"
print "<H1>This is my first CGI script</H1>"
print "Hello, world!"

address = None

def get_IP ():
    form = cgi.FieldStorage()
    if "ip_address" not in form: 
        print "<H1>Error</H1>"
        print ("Please fill in the name and addr fields.")
	return (None)
    else:
        return (form["ip_address"].value)

IP = get_IP ()
if IP != None:
    print "<p>name:", IP
