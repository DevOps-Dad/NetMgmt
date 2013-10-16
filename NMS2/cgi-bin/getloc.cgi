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
		<td class="style1"><strong>IP Address</strong></td>
		<td class="style1"><strong>MAC Address</strong></td>
		<td class="style1"><strong>Manufacturer</strong></td>
		<td class="style1"><strong>Edge Switch</strong></td>
		<td class="style1"><strong>Switch Port</strong></td>
		<td class="style1"><strong>Location</strong></td>
	</tr>
ENDHEAD

        # Get matching IP Address entries from Cisco core routers
        $ip_grep = `/bin/grep -w $location /var/www/html/arp/location.db `;
	@break = split (/\n/, $ip_grep);

	foreach $print (@break) {
		@ip_line = split (/;/, $print);
	        $juniper_mac = @ip_line[0];
       		$ip_address = @ip_line[1];
        	$switch_name = @ip_line[3];
        	$switch_port = @ip_line[4];
        	$location = @ip_line[5];

        	# Convert for OUI Search
        	$cisco_mac = Net::MAC->new('mac' => $juniper_mac);
        	$oui_mac = $cisco_mac->convert(
               		'base' => 16,
               		'bit_group' => 8,   
               		'delimiter' => '-'
        	);
                
                $mfg_arp = substr ($oui_mac, 0, 8);
                
                $oui_grep = `/bin/grep -i $mfg_arp /var/www/html/arp/* | /bin/sed 's_/var/www/html/arp/oui.txt:__' | /bin/sed 's_\(hex\)__'`;

                @break_oui = split (/  /, $oui_grep);


                $manufacturer = @break_oui[1];


  		print "<tr>";
        	print "<td class=\"style5\"><strong>$ip_address</strong></td>";
        	print "<td class=\"style5\"><strong>$juniper_mac</strong></td>";
        	print "<td class=\"style5\"><strong>$manufacturer</strong></td>";
        	print "<td class=\"style5\"><strong><a href=\"http://$switch_name.falconstor.net\">$switch_name</a></strong></td>";
        	print "<td class=\"style5\"><strong>$switch_port</strong></td>";
        	print "<td class=\"style5\"><strong>$location</strong></td>";
        	print "</tr>";
	}



