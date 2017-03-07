__author__ = 'Riccardo Frigerio'

'''
Oggetto LIMIT definito da file di testo
Attributi:
- bandwidth: quantita di traffico in KB da non superare nell'arco di un ciclo
- time: quantita di cicli in cui non superare la soglia
'''

class Limit(object):

    def __init__(self, bandwidth, time):
        self.bandwidth = int(bandwidth) * int(time)
        self.time = int(time)
