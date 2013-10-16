#!/usr/bin/perl 

use CGI qw(:standard);

$ip_add = param ('ip_add') || 'xxx';

$ENV{HOME} = '/home/apache';

print <<ENDHEAD;
        CTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
        <html xmlns="http://www.w3.org/1999/xhtml">

        <head>
        <meta http-equiv="Content-Language" content="en-us" />
        <meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
        <title>FalconStor Border Router Firewall</title>
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
                        font-size: large;
                }
                .style7 {
                        color: #FF0000;
                        text-align: center;
                }
                </style>

       </head>
       <body>
       <p class="style3"><strong>FalconStor Border Router Firewall</strong></p>
       <center><p class="style6"><strong>Existing Blocked Addresses</strong></p></center>
<center>
        <table border="1" style="width: 606px; height: 77px;">
                <tbody>
                        <tr>
                                <td style="font-weight: bold; text-align: center;">FALC-Border-01<br />
                                </td>
                                <td style="font-weight: bold; text-align: center;">FALC-Border-02<br />
                                </td>
                        </tr>
</center>
ENDHEAD

open (MYFILE, '>/var/www/cgi-bin/fwallout.txt');
print MYFILE "configure\n";
print MYFILE "delete policy-options prefix-list bad-guys $ip_add\n";
print MYFILE "commit confirmed 5\n";
print MYFILE "exit\n";
close (MYFILE);

@firewall_update1 = `/usr/local/rancid/bin/jlogin -f /var/www/cgi-bin/.cloginrc -x /var/www/cgi-bin/fwallout.txt 172.16.2.20`;
@firewall_update2 = `/usr/local/rancid/bin/jlogin -f /var/www/cgi-bin/.cloginrc -x /var/www/cgi-bin/fwallout.txt 172.16.2.21`;

@firewall_now1 = `/usr/local/rancid/bin/jlogin -c "show configuration policy-options prefix-list bad-guys" 172.16.2.20`;
@firewall_now2 = `/usr/local/rancid/bin/jlogin -c "show configuration policy-options prefix-list bad-guys" 172.16.2.21`;

foreach $firewall_out (@firewall_now1)
{
        if ($printcount++ >= 17)
        {
                if ($firewall_out == "")
                {
                        $printdone = 1;
                }

                if ($printdone != 1)
                {
                        print ('<tr>');
                        print "<td>$firewall_out</td>";
                        $print2 = $printcount-1;
                        print "<td>@firewall_now2[$print2]</td>";
                        print ('</tr>');
                }
        }
}

print <<ENDHEAD1
</tbody>
</table>
<br>
</center>
<form action="http://172.16.9.18/cgi-bin/zfirewallcommit.cgi"">
 <div class="style1"><strong></strong> &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
        <input type="submit" style="font-size: larger; background-color: #FF0000" value="***Press Here For Final Permanent Config Commit***"><br />
        <br />
</form>
<span class="style7"><strong>Submitted Changes Must Be Confirmed Within 5 Minutes or They Will Be Rolled Back</strong>

ENDHEAD1
