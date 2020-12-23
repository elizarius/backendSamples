#!/usr/bin/perl
#
# The traditional first program.

# Strict and warnings are recommended.
use strict;
use warnings;

my $p1 = "evtmd         1077        1     6264K  00:00:00.09    1.00%  run       00:16:07";
#my $p2:d = "rpad          1197        1     7432K  00:00:00.12    0.01%  run       00:16:00";
my $p3 = "com           1567        1    36160K  00:00:01.45    4.23%  run       00:15:59";



my $pos1 = index($p1, "%");
my $load = substr($p1,$pos1-4,4);
print ("AELZ_1: $load \n");

my $pos3 = index($p3, "%");
my $load1 = substr ($p3,$pos3-4,4);
print ("AELZ_2: $load1 \n");

my $load10 = $load1-$load;

print ("AELZ_3: $load10 \n");

my $tres = 5;
if ($load10 > $tres)  {
    print ("AELZ_4: $load10 \n");
} else {
    print ("AELZ_5: $tres \n");
}


