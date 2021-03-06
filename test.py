#!/usr/local/bin/python

import sys #needed for arguments
from pprint import pprint #needed to print data formats for figuring suff out
import re #regex wanted
import asa #libary for handling ASA configurations
import fgt #library for handling FGT configurations


'''
Purpose

    Test the libraries for the fw-conversion-library

Usage

    test.py <configfilename>

    test command
    python test.py ~/lstcasaconfig.txt

'''

def getopts(argv):
    '''Collect command-line options in a dictionary'''
    opts = {}  # Empty dictionary to store key-value pairs.
    opts["filename"] = argv.pop() # The filename for the config should be last, pop it off

    while argv:  # While there are arguments left to parse...
        if argv[0][0] == '-':  # Found a "-name value" pair.
            opts[argv[0]] = argv[1]  # Add key and value to the dictionary.
        argv = argv[1:]  # Reduce the argument list by copying it starting from index 1.

    return opts

# a dictionary of the cli arguments
opts = getopts(sys.argv)
# creates a string with the contents of filename from LCI options
in_config = open(opts["filename"], 'r').read()

obj_dict = asa.get_asa_net_obj(in_config) #Create a Dictionary of objects from the asa config

#pprint(obj_dict)

print(fgt.fgt_obj_str(obj_dict)) # write objects to fortigate format

#pprint.pprint(obj_dict)
