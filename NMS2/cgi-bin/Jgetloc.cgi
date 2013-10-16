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


$getloc = `/bin/grep -w $location /var/www/html/arp/desc/* | /bin/sed 's_/var/www/html/arp/desc/__'`;

$switch = substr($getloc, 0, 13);

$port = substr($getloc, 14, 9);

$mac_grep = `/bin/grep -w $port /var/www/html/arp/$switch`;

@break = split (/\n/, $mac_grep);
$mac_count = 0;
$ip_count = 0;
$oui_count = 0;
$final_count = 0;

foreach $line (@break) {
	@mac_break = split (/ /, $line);
	foreach $line1 (@mac_break){
		if ((substr($line1, 2, 1) eq ":") && substr($line1, 5, 1) eq ":") {
                	@mac_address[$mac_count] = $line1;
			$mac_count++;
		}
	}
}

foreach $find_ip (@mac_address) {
       	$juniper_mac = Net::MAC->new('mac' => $find_ip);
       	# Convert from Juniper to Cisco MAC format
       	$cisco_arp = $juniper_mac->convert(
      		'base' => 16,
       		'bit_group' => 16,
       		'delimiter' => '.'
       	);

       	$ip_grep = `/bin/grep $cisco_arp /var/www/html/arp/DC-Core-02 | /bin/sed 's_/var/www/html/arp/__'| /bin/sed 's_:Internet__' | /bin/sed 's_ARPA__'`;

        @break = split (/ /, $ip_grep);

        # Find and assign MAC Address in Net::MAC
        foreach $test (@break) {
               if ((substr($test, 1, 1) eq ".") || substr($test, 2, 1) eq ".") {
                        @cisco_ip[$ip_count] = $test;
 			$ip_count++;
		}
	}

        # Convert for OUI Search
        $oui_mac = $juniper_mac->convert(
                        'base' => 16,
                        'bit_group' => 8,
                        'delimiter' => '-'
                );

        $mfg_arp = substr ($oui_mac, 0, 8);

        $oui_grep = `/bin/grep -i $mfg_arp /var/www/html/arp/* | /bin/sed 's_/var/www/html/arp/oui.txt:__' | /bin/sed 's_\(hex\)__'`;

        @break_oui = split (/  /, $oui_grep);


        @manufacturer[$oui_count] = $break_oui[1];
	$oui_count++;
}

foreach $print (@mac_address) {
                print "<tr>";
                print "<td class=\"style5\"><strong>@cisco_ip[$final_count]</strong></td>";
                print "<td class=\"style5\"><strong>$print</strong></td>";
                print "<td class=\"style5\"><strong>@manufacturer[$final_count]</strong></td>";
                print "<td class=\"style5\"><strong>$switch</strong></td>";
                print "<td class=\"style5\"><strong>$port</strong></td>";
                print "<td class=\"style5\"><strong>$location</strong></td>";
                print "</tr>";
		
		$final_count++;
}



