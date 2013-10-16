#!/usr/bin/perl

## Null-router Version 1.0
## By Dan Mahoney
## Not licensed for redistribution
## Copyright 2004 Web Auction Inc

## Version 1.1 adds support for comment fields, minor email tweaks


$ENV{HOME} = "/root";
use DBI;

$version = "1.1";
@routers = ('172.16.2.1','172.16.2.3');
@badips = (@routers, '65.125.228.130');
$scripturl = $ENV{SCRIPT_NAME};


$sqlusername = "root";
$sqlpassword = "";
$databasename = "nullroutes";

&readparse;

if ($form{command} eq "listroutes") {
  &printheader;
  &showroutes;
  &printmainmenu;
}
elsif ($form{command} eq "addroute") {
  &printheader;
#  warn "Adding Route";
  &donull;  
  &logevent;
  &showroutes;
  &printmainmenu;
  &send_out_mail;
}
elsif ($form{command} eq "unroutedbonly") {
  &printheader;
  &rmdbroute;
  &logevent;
  &showroutes;
  &printmainmenu;
  &send_out_mail;
}
elsif ($form{command} eq "unroute") {
  &printheader;
  &undonull;
  &rmdbroute;
  &logevent;
  &showroutes;
  &printmainmenu;
  &send_out_mail;
}
elsif ($form{command} eq "showlogs") {
  &printheader;
  &showlogs;
  &printmainmenu;
}
else {
  &printheader;
  &showroutes;
  &printmainmenu;
}

sub showroutes {
  &connect;
  $query = "SELECT user, ip, FROM_UNIXTIME(UNIX_TIMESTAMP(time)) as formdate, id, comment FROM active;";
  $sth=$dbh->prepare($query);
  $sth->execute;
  if (@row = $sth->fetchrow_array) {
    print "<TABLE BORDER=1><TR><TD>IP Address</TD><TD>Added</TD><TD>Added by</TD><TD>Comment</TD>";
    print "<TD>&nbsp;</TD><TD>&nbsp;</TD></TR>";
    &printgridrow;  
    while(@row = $sth->fetchrow_array) {
      &printgridrow;
    }
    print "</TABLE>";
  }
  else {
    print "No Null Routes Found in DB";
  }
  &disconnect;
}

sub printheader {
  print "Content-type: text/html\n\n";
  print "<HTML>\n<HEAD>\n";
  print "<TITLE>Null-Router $version by Dan Mahoney -- ";
  print "Logged in as $ENV{REMOTE_USER}</TITLE>\n";
  print "<BODY BGCOLOR=\"#FDF9D9\">\n";
}

sub printrouteform {
  print "<FORM METHOD=POST ACTION=\"$scripturl\">\n";
  print "<INPUT TYPE=HIDDEN NAME=\"command\" VALUE=\"addroute\">";
  print "<FONT SIZE=+2>";
  print "<CODE>ROUTER# ip route <INPUT TYPE=TEXT SIZE=\"12\" NAME=\"ip\"> 255.255.255.255 Null0\n";
  print "(Reason: <INPUT TYPE=TEXT NAME=\"comment\">)</CODE></FONT><INPUT TYPE=SUBMIT VALUE=\"Null Route\">\n";
  print "</FORM>\n";
}

sub connect {
  $dbh = DBI->connect("DBI:mysql:$databasename", "$sqlusername", "$sqlpassword");
}

sub disconnect {
  $dbh->disconnect();
}

sub rmdbroute {
  &connect;
  &quotestuff;
  $query = "DELETE FROM active WHERE ip = $quoted{ip};";
  $sth = $dbh->prepare($query);
  $rv = $sth->execute;
  if ($rv) {
    print "Route deleted from db successfully\n<BR>";
  }
}

sub adddbroute {
  &connect;
  &quotestuff;
  $query = "INSERT INTO active (user, ip, action, comment) \
  VALUES ($quoted{remoteuser}, $quoted{ip}, $quoted{command}, $quoted{comment});";
#  warn "query is $query";
  $sth = $dbh->prepare($query);
  $rv = $sth->execute;
  if ($rv) {
    print "Route added to DB successfully\n<BR>";
  }
}

sub checkforbadips {
  $valid = 1;
  if (($form{ip} !~ m/^65.125.\d+.\d+/) && ($form{ip} !~ m/^66.199.\d+.\d+/)) {
    print "This is not a valid IP<BR>\n";
    $valid = 0;
  }
  foreach $badip (@badips) {
    if ($form{ip} eq $badip) {
      print "Stupid User Attempted to null-route $form{ip}<BR>\n";
      $valid = 0;
    }
  }
}


sub donull {
# at some point make this actually check IP ranges, rather then the simple pattern match.
# this will get annoying when we have more blocks.
  &checkforbadips;
  if ($valid eq 1) {
    $tempfilename = "/tmp/" . $$ . time;
    open CMDFILE, ">$tempfilename" or die "Unable to open temp file";
    print CMDFILE "config t\n";
    print CMDFILE "ip route $form{ip} 255.255.255.255 null0\n";
    print CMDFILE "exit\n";
    print CMDFILE "exit\n";
    close CMDFILE;

# Usage: /usr/local/rancid/bin/clogin [-autoenable] [-noenable] [-c command]  [-Evar=x] [-e enable-password] [-f 
# cloginrc-file] [-p user-password]  [-s script-file] [-t timeout] [-u username]  [-v vty-password] [-w enable-username] [-x 
# command-file]  [-y ssh_cypher_type] router [router...]
    print "<!-- #router spooge \n";
    foreach $routerip (@routers) {
      @args = ("/usr/local/rancid/bin/clogin", "-x", "$tempfilename", "-p", "Changer3247", "-u", "jgoldbrg", "-autoenable", $routerip);
      system(@args);
    }
    print "-->";

    &adddbroute;
    #&logevent;
    unlink $tmpfilename;
    print "Route Added Successfully<BR>\n";
  }
  else {
    &printmainmenu;
  }
}

sub undonull {
  $tempfilename = "/tmp/" . $$ . date;
  open CMDFILE, ">$tempfilename" or die "Unable to open temp file";
  print CMDFILE "config t\n";
  print CMDFILE "no ip route $form{ip} 255.255.255.255 null0\n";
  print CMDFILE "exit\n";
  print CMDFILE "exit\n";
  close CMDFILE;

  print "<!-- #router spooge \n";
  foreach $routerip (@routers) {
    @args = ("/usr/local/rancid/bin/clogin", "-x", "$tempfilename", $routerip);
    system(@args);
  }
  print "--> \n";

  print "Route deleted from router successfully<BR>\n";
  unlink $tmpfilename;
}

sub logevent {
  $query = "INSERT INTO log (remote_user, ip, command, remote_ip, comment) VALUES \
  ($quoted{remoteuser}, $quoted{ip}, $quoted{command}, $quoted{remote_addr}, $quoted{comment});";
  $sth = $dbh->prepare($query);
  $rv = $sth->execute;
  unless ($rv) {
    print "Unable to log $query into database";
  }
}

sub quotestuff {
  foreach $key (keys %form) {
    $quoted{$key} = $dbh->quote($form{$key})
  }
}



sub printgridrow {
  if ($row[4] eq "") {
    $row[4] = "<I>none listed</I>";
  }
  print "<TR><TD>$row[1]</TD><TD>$row[2]</TD><TD>$row[0]</TD><TD>$row[4]</TD>\n";
  print "<TD><A HREF=\"$scripturl?command=unroute&ip=$row[1]\">Un-Null-Route</A></TD>\n";
  print "<TD><A HREF=\"$scripturl?command=unroutedbonly&ip=$row[1]\">Un-Null-Route (DB Only)</A></TD>\n";
}


sub readparse {
  if ($ENV{'REQUEST_METHOD'} eq 'GET') {
    @pairs = split(/&/, $ENV{'QUERY_STRING'});
  } 
  elsif ($ENV{'REQUEST_METHOD'} eq 'POST') {
    read(STDIN, $buffer, $ENV{'CONTENT_LENGTH'});
    @pairs = split(/&/, $buffer);
  } 
  else {   
    # You can specify variables here if you're running this script from the command line.
    $form{firstname} = "michelle";
    $form{lastname} = "latta";
    $form{email} = "db\@cybernixie.com";
    #$form{command} = "randomize";
    # Or just have the script puke.
    &showroutes;
#    die "I dunno what kind of data you're handing me here.";
  } 

  foreach $pair (@pairs) {
    local($name, $value) = split(/=/, $pair);
    $name =~ tr/+/ /;
    $name =~ s/%([a-fA-F0-9][a-fA-F0-9])/pack("C", hex($1))/eg;
    $value =~ tr/+/ /;
    $value =~ s/%([a-fA-F0-9][a-fA-F0-9])/pack("C", hex($1))/eg;
    $value =~ s/<!--(.|\n)*-->//g;
    $form{$name} = $value;
  }        
  $form{remoteuser} = "$ENV{REMOTE_USER}";
  $form{remote_addr} = $ENV{REMOTE_ADDR};
  if (!defined $form{comment}) {
    $form{comment} = "";
  }
}
  

sub printmainmenu {
  print "<HR>";
  print "<A HREF=\"$scripturl?command=listroutes\">List Active Null-Routes</A> ||\n";
  print "<A HREF=\"$scripturl?command=showlogs\">Show Recent Logs</A>\n";
  print "<HR>\n";
  &printrouteform;
}


sub printfooter {
  print "</HTML></BODY>";
}

sub send_out_mail {
  open(MAIL,"|/usr/lib/sendmail -t");
  print MAIL "To: teh\@ezi.net\n";
  print MAIL "From: teh\@ezi.net (Network Engineering Server)\n";
  print MAIL "Subject: Web-Null Route\n";
  $time = localtime;
  print MAIL "$form{ip} was $form{command}'ed at $time by $form{remoteuser} via the web system\n";
  if ($form{comment} ne "") {
    print MAIL "Staff Comments: $form{comment}";
  }

}       

sub showlogs {
  &connect;
  undef @row;
  $query = "SELECT remote_ip, remote_user, command, ip,\
  FROM_UNIXTIME(UNIX_TIMESTAMP(timestamp)) as formdate, comment \
  FROM log ORDER BY timestamp DESC LIMIT 30;";
#  warn "query is $query";
  $sth=$dbh->prepare($query);
  $sth->execute or die "unable to execute";
  if (@row = $sth->fetchrow_array) {
    print "<TABLE BORDER=1><TR><TD>Remote IP</TD><TD>Remote User</TD><TD>Command</TD>";
    print "<TD>Affected IP</TD><TD>Date</TD><TD>Comment</TD></TR>\n";
    &printlogrow;  
    while(@row = $sth->fetchrow_array) {
      &printlogrow;
    }
    print "</TABLE>";
  }
  else {
    print "No Log Entries Found in DB";
  }
}

sub printlogrow {
  if ($row[5] eq "") {
    $row[5] = "<I>none listed</I>";
  }
  print "<TR><TD>$row[0]</TD><TD>$row[1]</TD><TD>$row[2]</TD>\n";
  print "<TD>$row[3]</TD><TD>$row[4]</TD><TD>$row[5]</TD></TR>\n";
}
