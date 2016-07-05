#!/usr/bin/python

def ipaddress(host):
    for k, v in host.iteritems():
        if k.startswith('ansible_enp'):
            return host[k]['ipv4']['address']
    return '127.0.0.1'

class FilterModule(object):
    ''' Ansible core jinja2 filters '''

    def filters(self):
        return {
                'ipaddress': ipaddress,
        }
