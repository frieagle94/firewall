# firewall
A custom application which implements functions of interactive routing and firewall, for the open source SDN controller Ryu.

L’idea dell’applicazione è quella di acquisire una richiesta da parte dell’utente tramite un file testuale da lui definito, che conterrà il valore della banda che TUTTI gli host non devono oltrepassare, e un secondo valore che, moltiplicato per 3, corrisponderà ai secondi consecutivi per cui l’host dovrà rimanere oltre quel limite.
L’applicazione otterrà la topologia della rete da un file testuale ottenuto da un servizio esterno, e utilizzerà il controller Ryu impostato come firewall. L’applicazione abiliterà il firewall e, inizialmente, consentirà la comunicazione tra tutti gli host.
Successivamente, entrerà in un ciclo infinito in cui continuerà a monitorare il traffico generato dagli host ed eventualmente li bloccherà se non rispettano le regole imposte.
Il blocco sarà rimosso dopo 15 secondi. In questo intervallo l’applicazione continua il monitoraggio per gli altri host.
L’applicazione è terminabile tramite KeyboardException. 

Di seguito la spiegazione di ogni package e modulo.

ENTRY POINT
 
Firewall.py
Parsa tramite i package FileHandler e Model, gli host e il limite imposto dall’utente e ne crea degli oggetti. Successivamente inizializza il firewall, setta tutti i permessi per far comunicare gli host e crea le regole di instradamento fra tutti gli host tramite il package NetworkHandler.
Effettua il monitoraggio del traffico ogni tre secondi, all’infinito. L’applicazione è terminabile tramite KeyboardException. 

Package: FileHandler

ReadFile.py
Definisce due metodi per l'apertura e chiusura dei file che contengono la topologia della rete

ParseObjects.py
Definisce due metodi per il parse di oggetti di host e limite definito da utente. Il limite è costituito da una banda e da un numero di cicli. L’idea è quella di bloccare un qualunque host che generi più di quella banda per un numero di cicli di monitoraggio consecutivi.

Package: Model
Host.py
Limit.py
Contiene due classi che definiscono l’oggetto Host, composto dal suo indirizzo MAC, dalla porta a cui collegato e dallo switch a cui è collegato, e l’oggetto Limit, composto banda e numero di cicli



Package: NetworkHandler

LogicHandler.py
Definisce una serie di metodi utili a gestire la logica dell'applicazione. Questi si occupano di inizializzare il firewall, settare i permessi di comunicazione, ottenere le statistiche per la misurazione del traffico, bloccare il traffico di un host se non rispetta i limiti, sbloccarlo dopo 15 secondi, aggiornare il log di traffico a video. Alcune di queste operazioni necessitano di comunicare con il controller; tali scambi sono eseguiti tramite REST chiamando metodi contenuti nel modulo successivo.

APIHandler.py
Definisce una serie di metodi utili a comunicare tramite REST con le API di Ryu. Ogni metodo costruisce l’URL relativo al comando da impartire, e l'eventuale corpo JSON se richiesto dall’interfaccia, per poi inoltrare la richiesta. Alcune richieste prevedono il parsing della successiva risposta, per ottenere le statistiche desiderate. Le 4 richieste principali gestite sono:
-> inizializzazione del firewall
-> settaggio permessi firewall (da tutti vs tutti all'inizio)
-> acquisizione statistiche traffico per ogni porta di ogni switch a cui è collegato un host
-> blocco di un host tramite firewall

Per capire quali URL e richieste utilizzare mi sono basato sulla documentazione consultabile qui:
FIREWALL -> https://osrg.github.io/ryu-book/en/html/rest_firewall.html

Voci utilizzate:
Inizializzare il firewall: https://osrg.github.io/ryu-book/en/html/rest_firewall.html#changing-enable-disable-state-of-all-switches
Creare una regola firewall: https://osrg.github.io/ryu-book/en/html/rest_firewall.html#id10

RYU_REST -> http://ryu.readthedocs.io/en/latest/app/ofctl_rest.html

Voci utilizzate:
Ottenere la statistica di traffico per ogni porta:
http://ryu.readthedocs.io/en/latest/app/ofctl_rest.html#get-ports-stats

