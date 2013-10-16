#!/bin/bash
cd /var/www/html/graphs/EdgeNonUni
/var/www/html/graphs/EdgeUtil/top-now.pl "Top Non-Unicast - Current" > index-now.html
/var/www/html/graphs/EdgeUtil/top-avg.pl "Top Non-Unicast - Daily Average" > index-avg.html


