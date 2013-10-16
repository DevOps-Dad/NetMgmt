#!/usr/bin/perl

#!/usr/bin/perl

## GetARP 1.1
## By Joe Goldberg
## Not licensed for redistribution
## Copyright 2008 FalconStor Software

use CGI qw(:standard);
use Net::MAC;

$switch_name = param('switch_name') || 'xxx';
$port_number = param('port_number') || 'xxx';

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

ENDHEAD

print "<p>Switch Name $switch_name</p>";
print "<p>Port Number $port_number</p>";

$sho_int = `env HOME=/home/apache /usr/local/rancid/bin/jlogin -c 'show ethernet-switching interfaces $port_number detail' $switch_name`;

@int_line = split (/\n/, $sho_int);

foreach $line (@int_line){
	print "<p>$line</p>";
}

print "<p>$sho_int</p>";


