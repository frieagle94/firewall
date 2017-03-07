import urllib2
import json
import requests
import re

__author__ = "Riccardo Frigerio"

# URL del controller
url_base = "http://localhost:8080/"

# METODO che inizializza il firewall
def startFirewall():

    # Costruisco l'URL della richiesta (TUTTI gli switch!)
    url_initialize = "firewall/module/enable/all"
    url = url_base + url_initialize
    
    # Invio via PUT della regola
    requests.put(url=url)

# METODO che tramite POST REST aggiunge una regola al firewall
def postFirewall(hostSRC, hostDST, rule):

    # Costruisco l'URL della richiesta (TUTTI gli switch!)
    url_rule = "firewall/rules/all"
    url = url_base + url_rule

    # Converto gli host in stringhe
    tmpSRC = str(hostSRC)
    tmpDST = str(hostDST)

    # Costruisco il corpo della richiesta
    if rule:
        json_root = {"dl_src": tmpSRC, "dl_dst": tmpDST, "dl_type" : "IPv4" }
    else:
        json_root = {"dl_src": tmpSRC, "dl_dst": tmpDST, "dl_type" : "IPv4", "actions": "DENY", "priority" : "10"}

    # Converto il corpo della richiesta in formato JSON
    json_data = json.dumps(json_root, sort_keys=False, indent=4, separators=(",", ": "))
    
    # Invio via POST della nuova regola
    reply_raw = requests.post(url=url, data=json_data)
    
    # Converto la risposta in formato JSON
    reply = reply_raw.json()
    
    # Ottengo la stringa che mi interessa
    toParse = reply[0]["command_result"][0]["details"]
    
    # Ritorno l'ID della regola inserita
    return int(re.split("=", toParse)[1])

# METODO che tramite DELETE REST rimuove una regola dal firewall
def deleteFirewall(rule_id):

    # Costruisco l'URL della richiesta (TUTTI gli switch!)
    url_delete = "firewall/rules/all"
    url = url_base + url_delete
    
    # Costruisco il corpo della richiesta
    json_root = {"rule_id": str(rule_id)}
    
    # Converto il corpo della richiesta in formato JSON
    json_data = json.dumps(json_root, sort_keys=False, indent=4, separators=(",", ": "))
    
    # Invio via DELETE della nuova regola
    requests.delete(url=url, data=json_data)

# METODO che tramite GET REST ritorna la statistica interessata
def getStats(port, dpid):

    # Costruisco l'URL della richiesta
    url_stats = "stats/port/"  + str(dpid)
    url = url_base + url_stats
    
    # Richiesta via GET della statistica
    reply = json.load(urllib2.urlopen(url=url))

    # Ritorno solo il valore interessato
    for item in reply[str(dpid)]:
        if item["port_no"] == int(port):
            return item["rx_bytes"]/1024
