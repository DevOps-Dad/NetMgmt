#!/usr/bin/perl

## ProcessARP 1.1
## By Joe Goldberg
## Not licensed for redistribution
## Copyright 2011 FalconStor Software

use CGI qw(:standard);
use Net::MAC;

$startsave = 0;

open (IPFILE, '/var/www/html/arp/FALC-Core-01');
open (IPOUTFILE, ">/var/www/html/arp/location.db");

while (<IPFILE>) {
	chomp;
	if (substr ($_, 0, 5) eq "Total") {
		$startsave = 0;
	}
        if ($startsave == 1) {
		$linepos = 0;
		@break = split (/ /, $_);
		foreach $param (@break) {
			if ($linepos == 2 && substr ($param, 0, 2) eq "vl") {
                                $vlan = $param;
                        }
                        if ($linepos == 1 && $param ne " ") {
                                $ip_address = $param;
                                $linepos++;
                        }
			if ($linepos == 0) {
				$mac_address = $param;
				$linepos++;
			}
		}
		$mac_grep = `/bin/grep $mac_address /var/www/html/arp/FALC-EC*`;
		if ($mac_grep eq "") {
			$mac_grep = `/bin/grep $mac_address /var/www/html/arp/FALC-WC*`;
			if ($mac_grep eq "") {
				$mac_grep = `/bin/grep $mac_address /var/www/html/arp/FALC-FL*`;
			}
		}
		@macbreak = split (/ /, $mac_grep);
		$macpos = 0;
		foreach $macparam (@macbreak) {
			if ($macpos == 1 && substr ($macparam, 0, 2) eq "ge") {
				chomp ($macparam);
				$mlength = length ($macparam);
				$length = $mlength - 3;
				$switch_port = substr ($macparam, 0, $length);
			}	
			if ($macpos == 0) {
				$switch_temp = substr ($macparam, 18);
				@switch_split = split (/:/, $switch_temp);		
				$switch = @switch_split [0];
				$macpos++;
			}
		}
		$space_grep = `/bin/grep -w $switch_port /var/www/html/arp/desc/$switch`;
		@location_temp = split (/up/, $space_grep);
		$loc_temp = @location_temp[2];
		$jack = substr ($loc_temp, 3);
		chomp ($jack);
                print IPOUTFILE "$mac_address;$ip_address;$vlan;$switch;$switch_port;$jack\n";
        }	
	if (substr ($_, 0, 3) eq "MAC") {
		$startsave = 1;	
	}
}

close (IPFILE);
close (IPOUTFILE);
