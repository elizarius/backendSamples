#!/usr/bin/perl
#
# The traditional first program.

# Strict and warnings are recommended.
use strict;
use warnings;

my $b = "dropped pkts out   : 1                  dropped pkts in    : 2";
my $drop_out = "dropped pkts out   : 0";
my $drop_in = "dropped pkts in   : 0";

    if ( !(scalar(grep /$drop_out/, $b)) ) {
        print("dropped out packets detected on DUT \n");
        print("$b \n");
    }
    if ( !(scalar(grep /$drop_in/, $b)) ) {
        print("dropped in packets detected on DUT \n");
        print("$b \n");
    }

print("AELZ done \n");
