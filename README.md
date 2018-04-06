# fw-conversion-library

This is a series of libraries to use in order to convert firewall configs from one Vendor to another. I am building this to improve my python skills.

It supports:  
ASA
Fortigate

# Network Object Dictionary Format

'''
name {
  type: fqdn,
  fqdn: FQDN_STR
}
name {
  type: "range",
  range first: FIRST_IP_STR
  range last: LAST_IP_STR
}
name {
  type: host,
  host: HOST_IP_STR
name {
  type: subnet
  network: NET_ADDR_STR
  prefixlen: PREFIX_LEN_STR  
}
'''
