#!/usr/bin/perl

print "</p>Getting ARP Table</p>";
system("/var/www/cgi-bin/getarp.sh");
print "</p>ARP repolling complete</p>";
print "Repolling Switches";
system("/var/www/cgi-bin/getvlan.sh");
print "<p>Polling Complete</p>";
