#!/usr/bin/perl

## GetLOC 1.0
## By Joe Goldberg
## Not licensed for redistribution
## Copyright 2008 FalconStor Software

use CGI qw(:standard);
use Net::MAC;

$location = param('location');

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
</style>

</head>
<body>
<p class="style3"><strong>IP and MAC Address Details</strong></p>
<p>&nbsp;</p>
<table style="width: 100%">
	<tr>
		<td class="style1"><strong>Switch</strong></td>
		<td class="style1"><strong>Switch Port</strong></td>
		<td class="style1"><strong>Admin Status</strong></td>
		<td class="style1"><strong>Port Status</strong></td>
		<td class="style1"><strong>Location</strong></td>
	</tr>
ENDHEAD

        # Get matching IP Address entries from Cisco core routers
        $ip_grep = `/bin/grep -w $location /var/www/html/arp/desc/* `;
	@break = split (/\n/, $ip_grep);

	foreach $print (@break) {
		@ip_line = split (' ', $print);
		@switch_split = split (':', @ip_line[0]);
		$switch_port = @switch_split[1];
		@switch_split_name = split ('/', @switch_split[0]);
		$switch_name = @switch_split_name[6];
	        $switch_presplit = @ip_line[0];
      		$admin_status = @ip_line[1];
        	$port_status = @ip_line[2];
        	$location = @ip_line[3];

  		print "<tr>";
		print "<td class=\"style5\"><strong><a href=\"http://$switch_name.falconstor.net\">$switch_name</a></strong></td>";
		print "<td class=\"style5\"><strong>$switch_port</strong></td>";
        	print "<td class=\"style5\"><strong>$admin_status</strong></td>";
        	print "<td class=\"style5\"><strong>$port_status</strong></td>";
        	print "<td class=\"style5\"><strong>$location</strong></td>";
	       	print "</tr>";

	}


