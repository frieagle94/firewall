__author__ = 'Riccardo Frigerio'

'''
Oggetto HOST
Attributi:
- mac_address: indirizzo MAC
- port: porta a cui e' collegato
- dpid: switch a cui e' collegato
'''

class Host(object):

    def __init__(self, mac_address, port, dpid):
        self.mac_address = mac_address
        self.port = port
        self.dpid = dpid
