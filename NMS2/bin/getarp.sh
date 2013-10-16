#!/bin/bash
/usr/local/rancid/bin/jlogin -c 'show arp | except 10.5.1 | except 10.1.3 | except 10.5.2 | except 70.42 | except 10.1.10 | except 10.1.1 | except 172.16 | except 10.9 | except 10.10 | except 10.11 | except 10.5.50 | except 10.5.3 | except 10.5.7' 172.16.2.30 > /var/www/html/arp/FALC-Core-01
/usr/local/rancid/bin/jlogin -c 'show arp | except 10.5.1 | except 10.1.3 | except 10.5.2 | except 70.42 | except 10.1.10 | except 10.1.1 | except 172.16 | except 10.9 | except 10.10 | except 10.11 | except 10.5.50 | except 10.5.3 | except 10.5.7' 172.16.2.31 > /var/www/html/arp/FALC-Core-02
/usr/local/rancid/bin/jlogin -c 'show ethernet-switching table | except ge-0/0/22 | except Flood' 172.16.9.32 > /var/www/html/arp/FALC-ECFL2-02
/usr/local/rancid/bin/jlogin -c 'show ethernet-switching table | except ge-0/0/22 | except Flood' 172.16.9.33 > /var/www/html/arp/FALC-ECFL2-03
/usr/local/rancid/bin/jlogin -c 'show ethernet-switching table | except ge-0/0/22 | except Flood' 172.16.9.34 > /var/www/html/arp/FALC-ECFL2-04
/usr/local/rancid/bin/jlogin -c 'show ethernet-switching table | except ge-0/0/22 | except Flood' 172.16.9.35 > /var/www/html/arp/FALC-ECFL2-05
/usr/local/rancid/bin/jlogin -c 'show ethernet-switching table | except ge-0/0/22 | except Flood' 172.16.9.36 > /var/www/html/arp/FALC-ECFL2-06
/usr/local/rancid/bin/jlogin -c 'show ethernet-switching table | except ge-0/0/22 | except Flood' 172.16.9.37 > /var/www/html/arp/FALC-ECFL2-07
/usr/local/rancid/bin/jlogin -c 'show ethernet-switching table | except ge-0/0/22 | except Flood' 172.16.9.38 > /var/www/html/arp/FALC-ECFL2-08
/usr/local/rancid/bin/jlogin -c 'show ethernet-switching table | except ge-0/0/22 | except Flood' 172.16.9.39 > /var/www/html/arp/FALC-ECFL2-09
/usr/local/rancid/bin/jlogin -c 'show ethernet-switching table | except ge-0/0/22 | except Flood' 172.16.9.40 > /var/www/html/arp/FALC-ECFL2-10
/usr/local/rancid/bin/jlogin -c 'show ethernet-switching table | except ge-0/0/22 | except Flood' 172.16.9.52 > /var/www/html/arp/FALC-WCFL2-02
/usr/local/rancid/bin/jlogin -c 'show ethernet-switching table | except ge-0/0/22 | except Flood' 172.16.9.53 > /var/www/html/arp/FALC-WCFL2-03
/usr/local/rancid/bin/jlogin -c 'show ethernet-switching table | except ge-0/0/22 | except Flood' 172.16.9.54 > /var/www/html/arp/FALC-WCFL2-04
/usr/local/rancid/bin/jlogin -c 'show ethernet-switching table | except ge-0/0/22 | except Flood' 172.16.9.55 > /var/www/html/arp/FALC-WCFL2-05
/usr/local/rancid/bin/jlogin -c 'show ethernet-switching table | except ge-0/0/22 | except Flood' 172.16.9.56 > /var/www/html/arp/FALC-WCFL2-06
/usr/local/rancid/bin/jlogin -c 'show ethernet-switching table | except ge-0/0/22 | except Flood' 172.16.9.57 > /var/www/html/arp/FALC-WCFL2-07
/usr/local/rancid/bin/jlogin -c 'show ethernet-switching table | except ge-0/0/22 | except Flood' 172.16.9.58 > /var/www/html/arp/FALC-WCFL2-08
/usr/local/rancid/bin/jlogin -c 'show ethernet-switching table | except ge-0/0/22 | except Flood' 172.16.9.59 > /var/www/html/arp/FALC-WCFL2-09
/usr/local/rancid/bin/jlogin -c 'show ethernet-switching table | except ge-0/0/22 | except Flood' 172.16.9.60 > /var/www/html/arp/FALC-WCFL2-10
/usr/local/rancid/bin/jlogin -c 'show ethernet-switching table | except ge-0/0/22 | except Flood' 172.16.9.61 > /var/www/html/arp/FALC-WCFL2-11
/usr/local/rancid/bin/jlogin -c 'show ethernet-switching table | except ge-0/0/22 | except Flood' 172.16.9.62 > /var/www/html/arp/FALC-WCFL2-12
/usr/local/rancid/bin/jlogin -c 'show ethernet-switching table | except ge-0/0/22 | except Flood | except ge-0/1/0 | except ge-0/1/1 | except ge-0/1/3' 172.16.9.71 > /var/www/html/arp/FALC-FL1-01
/usr/local/rancid/bin/jlogin -c 'show ethernet-switching table | except ge-0/0/22 | except Flood | except ge-0/1/0 | except ge-0/1/1 | except ge-0/1/3' 172.16.9.72 > /var/www/html/arp/FALC-FL1-02

/usr/local/rancid/bin/jlogin -c 'show interfaces descriptions' 172.16.9.32 > /var/www/html/arp/desc/FALC-ECFL2-02
/usr/local/rancid/bin/jlogin -c 'show interfaces descriptions' 172.16.9.33 > /var/www/html/arp/desc/FALC-ECFL2-03
/usr/local/rancid/bin/jlogin -c 'show interfaces descriptions' 172.16.9.34 > /var/www/html/arp/desc/FALC-ECFL2-04
/usr/local/rancid/bin/jlogin -c 'show interfaces descriptions' 172.16.9.35 > /var/www/html/arp/desc/FALC-ECFL2-05
/usr/local/rancid/bin/jlogin -c 'show interfaces descriptions' 172.16.9.36 > /var/www/html/arp/desc/FALC-ECFL2-06
/usr/local/rancid/bin/jlogin -c 'show interfaces descriptions' 172.16.9.37 > /var/www/html/arp/desc/FALC-ECFL2-07
/usr/local/rancid/bin/jlogin -c 'show interfaces descriptions' 172.16.9.38 > /var/www/html/arp/desc/FALC-ECFL2-08
/usr/local/rancid/bin/jlogin -c 'show interfaces descriptions' 172.16.9.39 > /var/www/html/arp/desc/FALC-ECFL2-09
/usr/local/rancid/bin/jlogin -c 'show interfaces descriptions' 172.16.9.40 > /var/www/html/arp/desc/FALC-ECFL2-10
/usr/local/rancid/bin/jlogin -c 'show interfaces descriptions' 172.16.9.52 > /var/www/html/arp/desc/FALC-WCFL2-02
/usr/local/rancid/bin/jlogin -c 'show interfaces descriptions' 172.16.9.53 > /var/www/html/arp/desc/FALC-WCFL2-03
/usr/local/rancid/bin/jlogin -c 'show interfaces descriptions' 172.16.9.54 > /var/www/html/arp/desc/FALC-WCFL2-04
/usr/local/rancid/bin/jlogin -c 'show interfaces descriptions' 172.16.9.55 > /var/www/html/arp/desc/FALC-WCFL2-05
/usr/local/rancid/bin/jlogin -c 'show interfaces descriptions' 172.16.9.56 > /var/www/html/arp/desc/FALC-WCFL2-06
/usr/local/rancid/bin/jlogin -c 'show interfaces descriptions' 172.16.9.57 > /var/www/html/arp/desc/FALC-WCFL2-07
/usr/local/rancid/bin/jlogin -c 'show interfaces descriptions' 172.16.9.58 > /var/www/html/arp/desc/FALC-WCFL2-08
/usr/local/rancid/bin/jlogin -c 'show interfaces descriptions' 172.16.9.59 > /var/www/html/arp/desc/FALC-WCFL2-09
/usr/local/rancid/bin/jlogin -c 'show interfaces descriptions' 172.16.9.60 > /var/www/html/arp/desc/FALC-WCFL2-10
/usr/local/rancid/bin/jlogin -c 'show interfaces descriptions' 172.16.9.61 > /var/www/html/arp/desc/FALC-WCFL2-11
/usr/local/rancid/bin/jlogin -c 'show interfaces descriptions' 172.16.9.62 > /var/www/html/arp/desc/FALC-WCFL2-12
/usr/local/rancid/bin/jlogin -c 'show interfaces descriptions' 172.16.9.71 > /var/www/html/arp/desc/FALC-FL1-01
/usr/local/rancid/bin/jlogin -c 'show interfaces descriptions' 172.16.9.72 > /var/www/html/arp/desc/FALC-FL1-02

/var/www/html/arp/processarp.pl
