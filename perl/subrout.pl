#!/usr/bin/perl
#
# The traditional first program.

# Strict and warnings are recommended.
use strict;
use warnings;


sub checkBasicIPv4Ping() {

    my $rs = 1;
    my ($ip1, $ip2);
    my $numArgs =  @_;
    if (@_ == 0) {
        ($ip1, $ip2) =("94.1.1.2","94.1.1.1");
    } else {
        ($ip1, $ip2) = @_;
    }

    print "N of arguments: $numArgs  args: $ip1  $ip2 \n";

    return $rs;
}

checkBasicIPv4Ping() ;

my @b = ("0.0.0.0", "1.1.1.1");
&checkBasicIPv4Ping(@b);
