
# This library will handle ASA objects and policy

import re # going to need regex
import ipaddress #need this for things and stuff.


def get_asa_net_obj(asa_config):
    '''
    receives a text asa configuration file as a string, returns a list with network object definitions

    Network objects include:
        FQDNs
        Network Objects
        Host Objects
        IP Address Ranges
    '''

    # network object regex string
    _RE_NETOBJECT_STR = r'^object\s+network\s+(.*)\s+(subnet|range|host|fqdn)\s+(.*)'
    # compiled network object regex
    _RE_NETOBJ = re.compile(_RE_NETOBJECT_STR, re.MULTILINE)
    # finds all the objects, but not descriptions, makes a list of tuples
    obj_list = _RE_NETOBJ.findall(asa_config)

    #
    # format for dictionary
    #
    # name: obj-GPYVPF201325BL {
    #   type: fqdn
    #   fqdn: GPYVPF201325BL.lstc.lesschwab.com
    # }
    #

    # dictionary of objects
    obj_dict = {}


    for i in obj_list: # for each object in the list
        obj_name_str = "".join(i[0]) #turn the tuple into a string
        obj_dict[i[0]] = {} #make a dictionary named after the object
        #obj_dict[i[0]]["name"] = i[0].rstrip() # the name of the object
        obj_dict[i[0]]["type"] = i[1] # the type of the object

        #clean up the data depending on the objects type
        if obj_dict[i[0]]["type"] == "fqdn":
            obj_dict[i[0]]["fqdn"] = re.split("\s|/",i[2]).pop()
        if obj_dict[i[0]]["type"] == "host":
            obj_dict[i[0]]["host"] = i[2]
        elif obj_dict[i[0]]["type"] == "subnet":
            network,subnet = re.split("\s|/",i[2])
            obj_dict[i[0]]["network"] = network
            obj_dict[i[0]]["prefixlen"] = ipaddress.ip_network(network + '/' + subnet).prefixlen #works for ipv4 and 6
        elif obj_dict[i[0]]["type"] == "range":
            range_first,range_last = i[2].split(" ")
            obj_dict[i[0]]["range first"] = range_first
            obj_dict[i[0]]["range last"] = range_last

    # return the dictionary of objects
    return obj_dict
