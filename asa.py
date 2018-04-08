
# This library will handle ASA objects and policy

import re # going to need regex
import ipaddress #need this for ip address handing
from pprint import pprint #needed to figure stuff out with dict/lists
from ciscoconfparse import CiscoConfParse #courtesy of github/mpenning

def get_asa_net_obj(asa_config):
    '''
    receives a text asa configuration file as a string, returns a list with network object definitions

    Network objects include:
        FQDNs
        Network Objects
        Host Objects
        IP Address Ranges
    '''

    # create the CiscoConfParse class object
    parsed_conf = CiscoConfParse(asa_config.splitlines())
    # create a list containg the network object lines and thier children
    obj_list = parsed_conf.find_children( "^object network\s" )

    # network object name regex string
    _RE_NETOBJ_NAME_STR = r'^object\s+network\s+(.*)'
    # compiled network object name compiled regex
    _RE_NETOBJ_NAME = re.compile(_RE_NETOBJ_NAME_STR)

    #network object type regex string, returns the type and data from this string
    _RE_NETOBJ_TYPE_STR = r'^(subnet|range|host|fqdn)\s+(.*)'
    #network compiled regex
    _RE_NETOBJ_TYPE = re.compile(_RE_NETOBJ_TYPE_STR)

    #network object description regex
    _RE_NETOBJ_DESC_STR = r'^description\s(.*)'
    #network object description
    _RE_NETOBJ_DESC = re.compile(_RE_NETOBJ_DESC_STR)

    #\s+(subnet|range|host|fqdn)\s+(.*)

    # dictionary of objects
    obj_dict = {}

    for line in obj_list: # for each object in the list
        line = line.lstrip() #remove the leading whitespace


        #get the important facts from the configuration lines
        if re.search(_RE_NETOBJ_NAME, line):
            obj_name = re.search(_RE_NETOBJ_NAME, line).group(1)
            obj_dict[obj_name] = {}
        elif re.search(_RE_NETOBJ_TYPE_STR, line):
            obj_type, obj_data = re.search(_RE_NETOBJ_TYPE_STR, line).group(1, 2)
            obj_dict[obj_name]['type'] = obj_type
            #obj_data needs to be further parsed
            if obj_type == "fqdn":
                obj_dict[obj_name]["fqdn"] = re.split("\s|/", obj_data).pop()
            elif obj_type == "host":
                obj_dict[obj_name]["host"] = obj_data
            elif obj_type == "subnet":
                network, subnet = re.split("\s|/", obj_data)
                obj_dict[obj_name]["network"] = network
                obj_dict[obj_name]["prefixlen"] = str(ipaddress.ip_network(network + '/' + subnet).prefixlen) #works for ipv4 and 6
            elif obj_type == "range":
                range_first, range_last = obj_data.split(" ")
                obj_dict[obj_name]["range first"] = range_first
                obj_dict[obj_name]["range last"] = range_last

        elif re.search(_RE_NETOBJ_DESC, line):
            obj_desc = re.search(_RE_NETOBJ_DESC, line).group(1)
            obj_dict[obj_name]["desc"] = obj_desc

    # return the dictionary of objects
    return obj_dict
