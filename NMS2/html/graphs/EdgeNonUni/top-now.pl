#!/usr/bin/perl

# Produces a secondary index page for a directory of MRTG html files.
# This index is in the form of a table of percent utilizations, sorted
# by the average in+out values read from the MRTG HTML pages.
#
# Uses the existing index.[s]html file to read the title, if a title
# is not specified on the command line.
#
# Run this script from within the directory you wish to index.
#
# Usage: findtops.pl [title] > index-sort.html

######################################################################

($title) = split(/\@/, $ARGV[0]);
# die <<USAGE unless $title;
# Usage: findtops.pl title > index-sort.html
# USAGE

foreach $file (`ls *.html *.shtml 2>/dev/null`) {
    chop($file);
    open(IN, $file) || die "$!: $file";
    if (($file =~ "index\.s?html") and (! $title)) {
	while (<IN>) {
	    if ( m|<TITLE>(.*)</TITLE>| ) {
		$title = $1;
		close(IN);
		next;
	    }
	}
    }
    $file =~ s/.html//;		# kludge for prettier output at the end

    while (<IN>) {
	last if /.Weekly. Graph/;    # just want daily
	# Brute force ... what the heck.
	#
	
	if (/.Description.:/) {
	    $_= <IN>;
	    $description{$file} = $1;
	    print $description{$file};
	}
	if (/Max.*In:/) {
	    $_ = <IN>;		     # numbers are on the next line
	    /\((\d+\.\d+)\%\)/;      # get "5.9" out of "9229.7 kb/s (5.9%)"
	    $maxin{$file} = $1;
	    $maxtot{$file} += $1;
	}
	
	if (/Max.*Out:/) {
	    $_ = <IN>;
	    /\((\d+\.\d+)\%\)/;
	    $maxout{$file} = $1;
	    $maxtot{$file} += $1;
	}

	if (/Average.*In:/) {	
	    $_ = <IN>;		
	    /\((\d+\.\d+)\%\)/;	
	    $avgin{$file} = $1;
	    $avgtot{$file} += $1;
	}
	
	if (/Average.*Out:/) {	
	    $_ = <IN>;		
	    /\((\d+\.\d+)\%\)/;	
	    $avgout{$file} = $1;
	    $avgtot{$file} += $1;
	}
	
	if (/Current.*In:/) {	
	    $_ = <IN>;		
	    /\((\d+\.\d+)\%\)/;	
	    $curin{$file} = $1;
	    $curtot{$file} += $1;
	}
	
	if (/Current.*Out:/) {	
	    $_ = <IN>;		
	    /\((\d+\.\d+)\%\)/;	
	    $curout{$file} = $1;
	    $curtot{$file} += $1;
	}
	
    }
    close(IN);
}


######################################################################

$date = `date`;

print <<HEAD;
<html>
<head>
<title>$title</title>
</head>
<body bgcolor="#FDF9D9">
<!--#include virtual="/mrtg/header.html"-->
<H1>$title</H1>

<h3>Sorted by current utilization</h3>

<p>$date</p>

<table border=1 cellpadding=2>
<tr><th>&nbsp;&nbsp;Interface&nbsp;&nbsp;</th> 
<th>&nbsp;&nbsp;AvgIn +<br>AvgOut&nbsp;&nbsp;</th> 
<th>&nbsp;&nbsp;AvgIn&nbsp;&nbsp;</th> 
<th>&nbsp;&nbsp;AvgOut&nbsp;&nbsp;</th> 
<th>&nbsp;&nbsp;MaxIn&nbsp;&nbsp;</th> 
<th>&nbsp;&nbsp;MaxOut&nbsp;&nbsp;</th>
<th>&nbsp;&nbsp;CurIn&nbsp;&nbsp;</th> 
<th>&nbsp;&nbsp;CurOut&nbsp;&nbsp;</th> 
<th>&nbsp;&nbsp;CurIn +<br>CurOut&nbsp;&nbsp;</th>
HEAD

######################################################################

foreach $file (sort { $curtot{$b} <=> $curtot{$a} } keys %curtot) {
print $file
    printf "<tr align=right><td align=left><a href=\"$file.html\">%s</a></td>", $file;
    printf "<td><b>%.1f%</b></td><td>%.1f%</td><td>%.1f%</td>", 
        $avgtot{$file}, $avgin{$file}, $avgout{$file};
    printf "<td>%.1f%</td><td>%.1f%</td><td>%.1f%</td><td>%.1f%</td><td><b>%.1f%</b></td></tr>\n",
        $maxin{$file}, $maxout{$file}, $curin{$file}, $curout{$file}, $curtot{$file};
}

######################################################################

print <<TAIL;
</table>
<!--#include virtual="/mrtg/footer.html"-->
</body>
</html>
TAIL


