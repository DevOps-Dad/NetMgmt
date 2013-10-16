#!/usr/bin/perl
# Checkpoint Firewall Switcher Script Thingy
# Shamlessly swiped and modified from Dan Mahoney's nullroute script
# Borked by Joe Goldberg
  
  $ENV{HOME} = "/var/www/html/lg";
  @routers = ('172.16.2.3');
  $tempfilename = "/tmp/" . $$ . time;
  open CMDFILE, ">$tempfilename" or die "Unable to open temporary file";
  print CMDFILE "write net\n";
  print CMDFILE "172.16.9.2\n";
  print CMDFILE "dc-core-02-confg\n";
  print CMDFILE "y\n";
  print CMDFILE "exit\n";
  close CMDFILE;
  print "Content-type: text/html\n\n";
#  print "<HTML>\n<HEAD>\n";
  print "<TITLE>Firewall Switcher 1.0 ";
  print "Logged in as </TITLE>\n";
  print "<BODY BGCOLOR=\"#C0C0C0\">\n";
#  print "<!-- router Spooge \n";
  foreach $routerip (@routers) {
    @args = ("/usr/local/rancid/bin/clogin", "-x", "$tempfilename", "-p", "Changer3247", "-u", "jgoldbrg", "-autoenable", $routerip);
    @status = `@args`;
    
    foreach $stat (@status) {
      print "$stat<BR>";
    }
  }
  
  unlink $tmpfilename;
#  print "-->";
  print "CheckPoint Firewall Now Default\n";
#  print "</HTML></BODY>";
