
# This library will handle ASA objects and policy

#import pprint to view dictionary
import pprint

# going to need regex
import re

'''
Create a Dictionary of commandline argument
'''

def get_asa_net_obj(asa_config):
    "receives a text asa configuration file, returns a list with network object definitions"

    #create a list for the objects
    #list because order for objects is not important
    #   for converting between vendors
    #objects is a list of dictionaries, each entry in the list
    #   is the name of the object
    objects = []

    #asa objects look like this:

    #object network host1
    # host 192.12.45.66
    #object network 10.10.0.0-19
    # subnet 10.10.0.0 255.255.224.0
    # description Local summarized net
    #object network Microsoft-Update
    # fqdn v4 update.microsoft.com




    #return the list of objects
    return objects


f = open('asa.txt', 'r')

print '\n'
pprint.pprint(asa_obj_in(f))
print '\n'
