#!/usr/bin/perl

##  ARPDB 1.1
## By Joe Goldberg
## Not licensed for redistribution
## Copyright 2011 FalconStor Software

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

# Sub IP Address

sub ip
{

