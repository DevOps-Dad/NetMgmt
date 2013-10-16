#!/usr/bin/perl

$ENV{HOME} = "/var/www/html/lg";
use DBI;

$version = "1.0";
@routers = ('172.16.2.3');
$scripturl = $ENV{SCRIPT_NAME};

$sqlusername = "root";
$sqlpassword = "";
$databasename = "firewall";

&printheader;
&printmainmenu;

if ($form{command} eq "checkpoint") {
	&printheader;
	&docheckpoint;
	&printmainmenu;
}
elsif ($form{command} eq "sonicwall") {
        &printheader;
        &dosonicwall;
        &printmainmenu;
}
elsif ($form{command} eq "null") {
        &printheader;
        &donull;
        &printmainmenu;
}
elsif ($form{command} eq "showlogs") {
        &printheader;
        &showroutes;
        &printmainmenu;
}

sub docheckpoint {

   # Create Temporary Command File
	$tempfilename = "/tmp/" . $$ . time;
	open CMDFILE, ">$tempfilename" or die "Unable to open temporary file";
	print CMDFILE "config t\n";
	print CMDFILE "route-map firewall-proxy permit 10\n";
	print CMDFILE "set ip default next-hop 10.10.1.11\n";
	print CMDFILE "exit\n";
	print CMDFILE "exit\n";
	print CMDFILE "exit\n";
	close CMDFILE;

   # Perform route-map cutover and spooge to page source
	print "<!-- #router Spooge \n";
	foreach $routerip (@routers) {
		@args = ("/usr/local/rancid/bin/clogin", "-x", "$tempfilename", "-p", "Changer3247", "-u", "jgoldbrg", "-autoenable", $routerip);
		system(@args);
	}
	print "-->";
	
	unlink $tmpfilename;

	print "Checkpoint Firewall Now Default\n";
}

sub dosonicwall {

   # Create Temporary Command File
        $tempfilename = "/tmp/" . $$ . time;
        open CMDFILE, ">$tempfilename" or die "Unable to open temporary file";
        print CMDFILE "config t\n";
        print CMDFILE "route-map firewall-proxy permit 10\n";
        print CMDFILE "set ip default next-hop 10.10.1.12\n";
        print CMDFILE "exit\n";
        print CMDFILE "exit\n";
        print CMDFILE "exit\n";
        close CMDFILE;

   # Perform route-map cutover and spooge to page source
        print "<!-- #router Spooge \n";
        foreach $routerip (@routers) {
                @args = ("/usr/local/rancid/bin/clogin", "-x", "$tempfilename", "-p", "Changer3247", "-u", "jgoldbrg", "-autoenable"
, $routerip);
                system(@args);
        }
        print "-->";

        unlink $tmpfilename;

        print "Sonicwall Firewall Now Default\n";
}

sub donull {

   # Create Temporary Command File
        $tempfilename = "/tmp/" . $$ . time;
	$fwstatefile = "/tmp/fwstate";
        open CMDFILE, ">$tempfilename" or die "Unable to open temporary file";
        print CMDFILE "config t\n";
        print CMDFILE "route-map firewall-proxy permit 10\n";
        print CMDFILE "set ip default next-hop null0\n";
        print CMDFILE "exit\n";
        print CMDFILE "exit\n";
        print CMDFILE "exit\n";
        close CMDFILE;

   # Perform route-map cutover and spooge to page source
        print "<!-- #router Spooge \n";
        foreach $routerip (@routers) {
                @args = ("/usr/local/rancid/bin/clogin", "-x", "$tempfilename", "-p", "Changer3247", "-u", "jgoldbrg", "-autoenable"
, $routerip);
                system(@args);
        }
        print "-->";

        unlink $tmpfilename;
	
        print "EMERGENCY INTERNET SHUTDOWN IN PLACE\n";
}

sub readparse {
  if ($ENV{'REQUEST_METHOD'} eq 'GET') {
    @pairs = split(/&/, $ENV{'QUERY_STRING'});
  } 
  elsif ($ENV{'REQUEST_METHOD'} eq 'POST') {
    read(STDIN, $buffer, $ENV{'CONTENT_LENGTH'});
    @pairs = split(/&/, $buffer);
  } 
}

sub printmainmenu {
	print "<HR>";
	print "<center><A HREF=\"$scripturl?command=checkpoint\"><img border=\"0\" src=\"/checkpoint.gif\"></A>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;\n";
  	print "<A HREF=\"$scripturl?command=sonicwall\"><img border=\"0\" src=\"/sonicwall.gif\"></A> &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;\n";
	print "<A HREF=\"$scripturl?command=null\"><img border=\"0\" src=\"/null.gif\"></A> </center>\n";
  	print "<HR>\n";
}

sub printheader {
	print "Content-type: text/html\n\n";
	print "<HTML>\n<HEAD>\n";
	print "<TITLE>Firewall Switcher $version ";
	print "Logged in as $ENV{REMOTE_USER}</TITLE>\n";
	print "<BODY BGCOLOR=\"#C0C0C0\">\n";
}

sub printfooter {
  print "</HTML></BODY>";
}
