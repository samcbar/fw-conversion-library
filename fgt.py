# This library will handle ASA objects and policy

import re # going to need regex
import ipaddress #need this for ip address handing
from pprint import pprint #helps with debugging



def fgt_obj_str(obj_dict):
    '''
    Create Fortigate objects from the object dictionary

    This will return a string with all of the objects which could be copied and pasted or otherwise used

    '''
    obj_str = "config firewall address\n" #config firewall address moves one into the address object area of the CLI

    for obj_name, obj_data in obj_dict.items():

        obj_str += "edit " + obj_name + "\n"

        if obj_data['type'] == "fqdn":
            obj_str += "set type fqdn\n"
            obj_str += "set fqdn " + obj_data['fqdn'] + "\n"

        elif obj_data['type'] == "host":
            obj_str += "set type ipmask \n" #fgt does not have a specific
            obj_str += "set subnet %s 255.255.255.255\n" %( obj_data['host'] )

        elif obj_data['type'] == "subnet":
            obj_str += "set type ipmask \n"
            netmask = ipaddress.ip_network(obj_data['network'] + '/' + obj_data['prefixlen']).netmask
            obj_str += "set subnet %s %s \n" %( obj_data['network'], netmask )

        elif obj_data['type'] == "range":
            obj_str += "set type iprange \n"
            obj_str += "set start-ip %s\n" %( obj_data['range first'] )
            obj_str += "set end-ip %s\n" %( obj_data['range last'] )

        if "desc" in obj_data:
                obj_str += "set comment %s\n" %( obj_data['desc'] )

    return obj_str
