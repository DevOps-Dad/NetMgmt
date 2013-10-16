#!/usr/bin/perl

## GetARP 1.1
## By Joe Goldberg
## Not licensed for redistribution
## Copyright 2008 FalconStor Software

use CGI qw(:standard);
use Net::MAC;

$ip_address = param('ip_address') || 'xxx';
$mac_address = param('mac_address') || 'xxx';

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
		<td class="style1"><strong>Core Router</strong></td>
		<td class="style1"><strong>MAC Address</strong></td>
		<td class="style1"><strong>Manufacturer</strong></td>
		<td class="style1"><strong>Edge Switch</strong></td>
		<td class="style1"><strong>Switch Port</strong></td>
		<td class="style1"><strong>Location</strong></td>
	</tr>
ENDHEAD

# Do we know the IP or MAC address
if ($ip_address ne "xxx") {
	&ip;
}

if ($mac_address ne "xxx") {
	&mac;
}


######################################
## Sub IP
## If the user entered an IP address
######################################

sub ip
{
	# Get matching IP Address entries from Cisco core routers
	$ip_grep = `/bin/grep -w $ip_address /var/www/html/arp/* | /bin/sed 's_/var/www/html/arp/__'| /bin/sed 's_:Internet__' | /bin/sed 's_ARPA__'`;
	@ip_line = split (/\n/, $ip_grep);

	foreach $line (@ip_line){
		@break = split (/ /, $line);

		
		# Find and assign MAC Address in Net::MAC
		foreach $test (@break) {
			if ((substr($test, 4, 1) eq ".") && substr($test, 9, 1) eq ".") {
				$cisco_mac = Net::MAC->new('mac' => $test);
			}
			if (substr($test, 0, 1) eq "V"){
				$vlan = $test;
			}
		}

		$router = $break[0];

		# Convert from Cisco to Juniper MAC format
		$new_mac = $cisco_mac->convert(
		'base' => 16,
          	'bit_group' => 8, 
          	'delimiter' => ':'
  		);	
		
		# Get Juniper matching MAC addresses
		$mac_grep = `/bin/grep $new_mac /var/www/html/arp/* | /bin/sed 's_/var/www/html/arp/__'`;
		
		@mac_line = split (/\n/, $mac_grep);
	
		foreach $mline (@mac_line){
		
			@mac_break = split (/ /, $mline);
		
			foreach $mac_line (@mac_break) {

				if (substr($mac_line, 0, 4) eq "FALC") {
					$temp_switch_name = $mac_line;
				}

                	        if ((substr($mac_line, 2, 1) eq ":") && substr($mac_line, 5, 1) eq ":") {
                        	        $temp_juniper_mac = $mac_line;
				}

				if ((substr($mac_line, 0, 1) eq "g") && substr($mac_line, 1, 1) eq "e") {
                                	$temp_switch_port = $mac_line;
					
                               	        if ((substr($temp_switch_port, 7, 2) ne "22") && (substr($temp_switch_port, 7, 2) ne "23")) {
						$switch_port = substr($temp_switch_port, 0, - 3);
						$switch_name = substr($temp_switch_name, 0, - 1);
						$juniper_mac = $temp_juniper_mac;
                                	}
				}
				
			}
		}			

		# Convert for OUI Search
        	$oui_mac = $cisco_mac->convert(
            		'base' => 16,
            		'bit_group' => 8,   
           		'delimiter' => '-'
        	);
                
        	$mfg_arp = substr ($oui_mac, 0, 8);
                
        	$oui_grep = `/bin/grep -i $mfg_arp /var/www/html/arp/* | /bin/sed 's_/var/www/html/arp/oui.txt:__' | /bin/sed 's_\(hex\)__'`;

        	@break_oui = split (/  /, $oui_grep);


        	$manufacturer = $break_oui[1];

		# Get Location

                $loc = `/bin/grep -w $switch_port /var/www/html/arp/desc/$switch_name`;

                $location = substr($loc, -7);

		print "<tr>";
		print "<td class=\"style5\"><strong>$ip_address</strong></td>";
		print "<td class=\"style5\"><strong>$router</strong></td>";
		print "<td class=\"style5\"><strong>$juniper_mac</strong></td>";
		print "<td class=\"style5\"><strong>$manufacturer</strong></td>";
		print "<td class=\"style5\"><strong>$switch_name</strong></td>";
		print "<td class=\"style5\"><strong>$switch_port</strong></td>";
		print "<td class=\"style5\"><strong>$location</strong></td>";
		print "</tr>";

	}
}

######################################
## Sub MAC
## If the user entered an IP address
######################################

sub mac 
{
	# Is it Juniper or Cisco format
	$user_mac = Net::MAC->new('mac' => $mac_address);
	$bits = $user_mac->get_bit_group;
	if ($bits == 8) {
                # Convert from Juniper to Cisco MAC format
                $cisco_arp = $user_mac->convert(
                'base' => 16,
                'bit_group' => 16,
                'delimiter' => '.'
                );

		$juniper_arp = $user_mac;
	} 
	elsif ($bits == 16) {

	   	# Convert from Cisco to Juniper MAC format
                $juniper_arp = $user_mac->convert(
                'base' => 16,
                'bit_group' => 8,
                'delimiter' => ':'
                ); 

		$cisco_arp = $user_mac;
	} 
	elsif ($bits == 0) {
		print "<p>Incorrectly formatted MAC Address</p>";
	}
	
        # Get matching IP Address entries from Cisco core routers
        $mac_grep = `/bin/grep $cisco_arp /var/www/html/arp/* | /bin/sed 's_/var/www/html/arp/__'| /bin/sed 's_:Internet__' | /bin/sed 's_ARPA__'`;

        @ip_line = split (/\n/, $mac_grep);

        foreach $line (@ip_line){
                @break = split (/ /, $line);

                # Find and assign MAC Address in Net::MAC
                foreach $test (@break) {
                        if ((substr($test, 1, 1) eq ".") || substr($test, 2, 1) eq ".") {
                                $cisco_ip = $test;
                        }
                        if (substr($test, 0, 1) eq "V"){
                                $vlan = $test;
                        }
                }

                $router = $break[0];

                $jun_mac_grep = `/bin/grep $juniper_arp /var/www/html/arp/* | /bin/sed 's_/var/www/html/arp/__'`;
		
		@jun_mac_line = split (/\n/, $jun_mac_grep);

		foreach $jline (@jun_mac_line){
		
	                @jun_mac_break = split (/ /, $jline);

        	        foreach $mac_line (@jun_mac_break) {
				if (substr($mac_line, 0, 4) eq "FALC") {
                                        $temp_switch_name = $mac_line;
                                }
                	        if ((substr($mac_line, 0, 1) eq "g") && substr($mac_line, 1, 1) eq "e") {
                        	        $temp_switch_port = $mac_line;
					
					if ((substr ($temp_switch_port, 7, 2)  ne "22") && (substr ($temp_switch_port, 7, 2)  ne "23")) {
                                                $switch_port = substr($temp_switch_port, 0, - 3);
                                                $switch_name = substr($temp_switch_name, 0, - 1);
					}
                      	        }
				

               		 }
		}

                # Convert for OUI Search
                $oui_mac = $user_mac->convert(
                        'base' => 16,
                        'bit_group' => 8,
                        'delimiter' => '-'
                );

                $mfg_arp = substr ($oui_mac, 0, 8);

                $oui_grep = `/bin/grep -i $mfg_arp /var/www/html/arp/* | /bin/sed 's_/var/www/html/arp/oui.txt:__' | /bin/sed 's_\(hex\)__'`;

                @break_oui = split (/  /, $oui_grep);


                $manufacturer = $break_oui[1];

		# Get Location
		$loc = `/bin/grep -w $switch_port /var/www/html/arp/desc/$switch_name`;

		$location = substr($loc, -7);

                print "<tr>";
                print "<td class=\"style5\"><strong>$cisco_ip</strong></td>";
                print "<td class=\"style5\"><strong>$router</strong></td>";
                print "<td class=\"style5\"><strong>$juniper_arp</strong></td>";
		print "<td class=\"style5\"><strong>$manufacturer</strong></td>";
                print "<td class=\"style5\"><strong>$switch_name</strong></td>";
                print "<td class=\"style5\"><strong>$switch_port</strong></td>";
                print "<td class=\"style5\"><strong>$location</strong></td>";
                print "</tr>";
		
	}

}

