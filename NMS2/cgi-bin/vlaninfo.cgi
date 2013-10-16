#!/usr/bin/perl

## VLANInfo 1.0
## By Joe Goldberg
## Not licensed for redistribution
## Copyright 2008 FalconStor Software

use CGI qw(:standard);
use Net::MAC;

$vlan_name = param('vlan_name') || 'xxx';

# Print HTML Header
print <<ENDHEAD;
CTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml">

<head>
<meta http-equiv="Content-Language" content="en-us" />
<meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
<title>FalconStor IP and MAC Address Details</title>
<style type="text/css">
.style1 {
        text-align: center;
        font-size: large;
        border-width: 2px;
        background-color: #FFFF99;
}
.style3 {
        text-align: center;
        font-size: x-large;
}
.style5 {
        text-align: center;
        border-width: 2px;
}
.style6 {
	background-color: #0000FF;
        text-align: center;
        border-width: 2px;
}
.style7 {
	background-color: #00FF00;
        text-align: center;
        border-width: 2px;
}
	
</style>

</head>
<body>
<p class="style3"><strong>Port Mappings for $vlan_name</strong></p>
<p>&nbsp;</p>
<table style="width: 100%">
        <tr>
                <td class="style1"><strong>Switch Name</strong></td>
                <td class="style1"><strong>Switch Port</strong></td>
        </tr>
ENDHEAD


$got_it = 0;

$dirpath="/var/www/html/arp/vlan/";

opendir(IN,"$dirpath") or die "opening directory failed:$!";

while (defined ($file = readdir(IN)) ) {
	@files=split / /,$file;
	
	foreach $filename (@files)
	{
		open (INPUT, "$dirpath".$filename) or warn "Can't open the file $filename\n:$!";
		until (eof(INPUT)) {
			chomp($line = <INPUT>);
			$vlan = substr($line, 0, 6);

			if ($vlan eq $vlan_name) {
				$got_it = 1;
			} elsif ($got_it == 1) {
				if (substr($vlan, 0, 1) ne "V") {
					@ports[$count] = $line;
					$count++;
				} else {
					$got_it = 0;
					$count = 0;
				}
			}
		}

		foreach $print (@ports) {
			if (substr($filename, 0, 1) eq "F") {
				print "<p>FileName: $filename   VLAN: $vlan_name    Ports: $print</p>";
			}
		}
	}
}
 
closedir(IN);
