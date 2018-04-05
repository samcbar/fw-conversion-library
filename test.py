#!/usr/local/bin/python

import sys #needed for arguments
import pprint #needed to print data formats for figuring suff out
import re #regex wanted
import json #we will structure the data in a json format
import ipaddress #need this for things and stuff.
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
# network object regex string
_RE_NETOBJECT_STR = r'^object\s+network\s+(.*)\s+(subnet|range|host|fqdn)\s+(.*)'
# compiled network object regex
_RE_NETOBJ = re.compile(_RE_NETOBJECT_STR, re.MULTILINE)
# finds all the objects, but not descriptions, makes a list of tuples
obj_list = re.compile(_RE_NETOBJ).findall(in_config)

# format for data wanted
# {
#   objects {
#       name: obj-GPYVPF201325BL {
#           type: fqdn
#           fqdn: GPYVPF201325BL.lstc.lesschwab.com
#       }
#   }
# }
#

# dictionary of objects
obj_dict = {}

for i in obj_list: # for each object in the list
    obj_name_str = "".join(i[0]) #turn the tuple into a string
    obj_dict[i[0]] = {} #make a dictionary named after the object
    obj_dict[i[0]]["name"] = i[0].rstrip() # the name of the object
    obj_dict[i[0]]["type"] = i[1] # the type of the object

    #if obj_dict[i[0]]["type"] == "fqdn":

    #elif obj_dict[i[0]]["type"] == "host":

    if obj_dict[i[0]]["type"] == "subnet":
        network,subnet = re.split(" |/",i[2])
        obj_dict[i[0]]["network"] = network
        obj_dict[i[0]]["prefixlen"] = ipaddress.ip_network(network + '/' + subnet).prefixlen #works for ipv4 and 6
        pprint.pprint(obj_dict[i[0]])
    elif obj_dict[i[0]]["type"] == "range":
        range_first,range_last = i[2].split(" ")
        obj_dict[i[0]]["range first"] = range_first
        obj_dict[i[0]]["range last"] = range_last


    #obj_dict[i[0]]["data"] = i[2] # the data of the object



#for k, v in obj_dict.items():
#    print(k, v)
#pprint.pprint(obj_dict["obj-ok2static-oktacdn-com.name"])
#pprint.pprint(obj_dict[obj-ok2static-oktacdn-com.type])
#pprint.pprint(obj_dict[obj-ok2static-oktacdn-com.data])
