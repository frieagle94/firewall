import os
import json

from NetworkHandler import APIHandler

__author__ = 'Riccardo Frigerio'

traffic = {}    # Dizionario per tenere conto delle ultime rilevazioni di traffico prodotto dai vari host
DoS = {}        # Dizionario degli host bloccati con relativo tempo di blocco
DoSRule = {}    # Dizionario degli host bloccati con relative regole di blocco

current_time = 0    # Tengo traccia del tempo per poter calcolare se il traffico e' eccessivo

# METODO che inizializza il firewall consentendo la comunicazione tra tutti gli host
def initializeFirewall(hosts):
    
    print "[Firewall] Initializing firewall..."
    
    # Abilito il firewall su tutti gli switch
    APIHandler.startFirewall()

    # Creo una lista di log per tenere traccia del traffico effettuato dagli host
    for host in hosts:
        traffic[host] = []
    
    print "[Firewall] Allowing communication between hosts..."
    
    # Abilito le comunicazioni tra tutti gli host
    for src in hosts:
        for dst in hosts:
            # POST della regola in entrambi i sensi
            APIHandler.postFirewall(src, dst, True)
            APIHandler.postFirewall(dst, src, True)

# METODO che monitora, ogni 3 secondi, il traffico generato da ogni host ed, eventualmente, lo blocca
def monitorHosts(hosts, limit):

    global current_time # Acquisisco la variabile globale

    # Per ogni host, acquisisco la statistica di traffico
    for host in sorted(hosts.keys()):
    
        if current_time < limit.time:
            # GET della statistica di traffico, appendendo per la prima volta alla lista il valore
            traffic[host].append(APIHandler.getStats(hosts[host].port, hosts[host].dpid))

            if current_time == 0:   # Alla prima rilevazione, stampo il log a video 
                 print "Host: ", host, " Traffic: ", (traffic[host][current_time]), "KB"

        else:
            # GET della statistica di traffico, aggiornando il valore nella lista
            traffic[host][current_time%limit.time] = APIHandler.getStats(hosts[host].port, hosts[host].dpid) 

    updateConsole(traffic, limit)    # Aggiorno il log a video

    # Faccio il controllo solo se e' passato un tempo sufficientemente lungo dall'inizio dell'esecuzione
    if current_time >= limit.time:
        for host in traffic:
            
            # Se l'host e' bloccato, controllo da quanto
            if host in DoS.keys():
                
                # Se e' bloccato da 15 secondi, lo sblocco
                if current_time - DoS[host] == 5:
                    print "[DoS] Safety time expired, going to unblock ", host, "..."
                    unblockHost(host)

            # Se non e' bloccato, controllo quanto traffico ha generato negli ultimi limit.time*3 secondi
            else:
                if current_time%limit.time == 4:
                    tmp = 0
                else:
                    tmp = current_time%limit.time + 1
            
                # Se il traffico supera la soglia impostata dall'utente, blocco l'host
                if (traffic[host][current_time%limit.time] - traffic[host][tmp]) >= limit.bandwidth:
                    print "[DoS] Possible DoS detected: going to block", host, "..."
                    blockHost(hosts[host].mac_address, hosts)

    # Incremento il tempo corrente
    current_time = current_time + 1

# METODO che blocca il traffico proveniente da un host
def blockHost(host, hosts):
    
    DoS[host] = current_time    # Aggiungo l'host ai bloccati e memorizzo il tempo corrente
    DoSRule[host] = []          # Inizializzo la lista delle regole di blocco per l'host bloccato
    
    # Blocco del traffico proveniente dall'host incriminato vs tutti
    for dst in hosts:
        rule_id = APIHandler.postFirewall(host, dst, False)    # POST regola di blocco
        DoSRule[host].append(rule_id)                          # Aggiungo l'id della regola poi sbloccare agevolmente
    
    print "[DoS] ", host, "blocked."

# METODO che sblocca il traffico proveniente da un host
def unblockHost(host):
 
    # Acquisisco la lista di regole di blocco e le cancello tutte
    for rule_id in DoSRule[host]:
        APIHandler.deleteFirewall(rule_id)    # DELETE regola di blocco
    
    # Rimuovo l'host da tutte le blacklist
    del DoS[host]
    del DoSRule[host]
    print "[DoS] ", host, "unblocked."

# METODO che aggiorna il log a video del traffico
def updateConsole(traffic, limit):
    os.system("clear")
    global current_time
    
    for host in sorted(traffic.keys()):
        print "Host: ", host, " Traffic: ", (traffic[host][current_time%limit.time]), "KB"    # Stampa del traffico per ogni host
    
    for host in DoS.keys():
        print "[DoS] ", host, "currently blocked for other", (5 - (current_time - DoS[host]))*3 , "seconds." # Stampa host DoS
