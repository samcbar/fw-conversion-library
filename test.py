#!/usr/local/bin/python

import sys #needed for arguments
import pprint #needed to print a dictionary
import re #regex wanted
'''
Purpose

    Test the libraries for the fw-conversion-library

Usage

    test.py <configfilename>

    test command
    python test.py ~/lstcasaconfig.txt

'''

'''Collect command-line options in a dictionary'''

def getopts(argv):
    opts = {}  # Empty dictionary to store key-value pairs.
    opts["filename"] = argv[-1] # The filename for the config should be last

    while argv:  # While there are arguments left to parse...
        if argv[0][0] == '-':  # Found a "-name value" pair.
            opts[argv[0]] = argv[1]  # Add key and value to the dictionary.
        argv = argv[1:]  # Reduce the argument list by copying it starting from index 1.

    return opts


opts = getopts(sys.argv) # a dictionary of the cli arguments

print "\n"
pprint.pprint(opts)
print "\n"

in_config = open(opts["filename"], 'r').read() # creates a string with the contents of filename



objects = re.compile(r"^\s*object network .*").findall(in_config) #finds all the lines that have object followed by a space

#print in_config
#print objects
print type(in_config)
print len(objects)


print objects[0]
print objects[int(round(len(objects)/2))]
print objects[-1]
