#!/usr/bin/perl
	print "Content-type: text/html\n\n";
	print "<HTML>\n<HEAD>\n";
	print "<TITLE>Firewall Switcher 1.0 ";
	print "Logged in as </TITLE>\n";
	print "<BODY BGCOLOR=\"#C0C0C0\">\n";
	@routers = ('172.16.2.3');
        $tempfilename = "/tmp/" . $$ . time;
        open CMDFILE, ">$tempfilename" or die "Unable to open temporary file";
        print CMDFILE "config t\n";
	print CMDFILE "no route-map firewall-proxy permit 10\n";
        print CMDFILE "route-map firewall-proxy permit 10\n";
	print CMDFILE "match ip address 50\n";
        print CMDFILE "set ip default next-hop 10.10.1.11\n";
        print CMDFILE "exit\n";
        print CMDFILE "exit\n";
        print CMDFILE "exit\n";
        close CMDFILE;

   # Perform route-map cutover and spooge to page source
        print "router Spooge \n";
        foreach $routerip (@routers) {
                @args = ("/usr/local/rancid/bin/clogin", "-x", "$tempfilename", "-p", "Changer3247", "-u", "jgoldbrg", "-autoenable"
, $routerip);
                system(@args);
        }

        unlink $tmpfilename;

        print "CheckPoint Firewall Now Default\n";
	print "</HTML></BODY>";
