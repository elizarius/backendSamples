#!/usr/bin/perl
#
# The traditional first program.

# Strict and warnings are recommended.
use strict;
use warnings;

# Print a message.
my %zz = (
        red => 1,
        green => 2,
        blue => 3,);
my $rs = scalar keys %zz;
print "nKeys = $rs \n";
