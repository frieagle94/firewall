import time

from FileHandler import ParseObjects
from NetworkHandler import LogicHandler

__author__ = 'Riccardo Frigerio'

# Per catturare l'interruzione del programma tramite pressione di CTRL+c
try:

    print "[Firewall] Acquiring topology..."

    # Ottengo una lista degli host connessi alla rete
    hosts = ParseObjects.getHosts()

    # Ottengo il limite definito da utente
    limit = ParseObjects.getLimit()

    # Se e' la prima volta che lancio il programma, consento tutte le comunicazioni, senno' effettuo il monitoraggio
    LogicHandler.initializeFirewall(hosts)  # Imposto il firewall da 0

    print "[Firewall] DONE."
    
    print "[Firewall] Initializing monitoring..."
    
    time.sleep(0.5)

    #ciclo infinito serve per continuare il monitoraggio
    while True:
        LogicHandler.monitorHosts(hosts, limit) # Continuo il monitoraggio in cerca di magagne
        
        # Rieseguo il monitoraggio una volta ogni 3 secondi
        time.sleep(1)
        
        print "[Firewall] Refresh in 2 seconds..."
        time.sleep(1)
        
        print "[Firewall] Refresh in 1 second..."
        time.sleep(1)

except KeyboardInterrupt:
    print "Esecuzione del firewall terminata."
