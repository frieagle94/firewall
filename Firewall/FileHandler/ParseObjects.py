import re
import json
import os

from FileHandler import ReadFile
from Model.Host import Host
from Model.Limit import Limit

__author__ = 'Riccardo Frigerio'

# METODO per il parsing di tutti gli host da Host.txt
def getHosts():

    filename = "Host.txt"

    # Apertura file
    in_file = ReadFile.openFile(filename)
    
    # Inizializzazione dizionario host
    hosts = {}
    
    # Lettura di tutte le linee del file
    for line in in_file:
        mac_address = re.split("[= ]+", line)[2]
        port = re.split("[= ]+", line)[4]
        dpid = re.split("[= >]+", line)[6]
        
        # Inserimento dell'host parsato
        hosts[mac_address] = Host(mac_address, int(port), int(dpid))

    # Chiusura file
    ReadFile.closeFile(in_file)

    return hosts

# METODO Per il parsing del limite da Limit.txt
def getLimit():

    filename = "Limit.txt"

    # Apertura file
    in_file = open(filename, "r")
    
    for line in in_file:
        content = re.split(",", line)
        break    

    # Creazione del limite dai valori parsati
    limit = Limit(bandwidth=int(content[0]),time=int(content[1]))
    
    # Chiusura file
    in_file.close()
    
    return limit
