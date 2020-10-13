#!/bin/bash

# Get pseudorandom string 64 bits by urandom

head -c 1000 /dev/urandom | tr -dc 'a-zA-Z0-9~!/+-@#$%^&*_' | fold -w 64 | head -n 1|  tr -d '\n'

#TEST_IP=$(kubectl -n zz describe  pod test-cc  | grep "IP" | cut -d':' -f 2  | sed -e 's/^[ \t]*//')
#echo "$TEST_IP"

