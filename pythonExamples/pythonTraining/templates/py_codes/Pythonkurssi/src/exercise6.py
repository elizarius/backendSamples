#! /usr/bin/python
# -*- coding: iso-8859-1 -*-

# exercise6.py
# exercise 6 with modules
# Copyright Tieturi Oy 2010

import conv.fahreheits as converter

def query_range():
    range_start = input("Give the range start: ")
    range_end = input("Give the range end: ")
    return range_start, range_end

def main():
    """main function"""    
    start, end = query_range()
    converter.print_fahrenheits(start, end)

if __name__ == "__main__":
    main()