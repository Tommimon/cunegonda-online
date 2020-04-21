# contiene i dati pubblici per tutti

from replicated.player_public import *
from tcp_basics import Replicator, ReplicatedVar

# FASI
ATTESA_GIOCATORI = 1
PASSAGGIO_CARTE = 2
GIOCO = 3
FINE_PARTITA = 4


class GameState:
    def __init__(self, auth=False):
        self.replicator = Replicator('game_state', auth=auth)
        self.cont_partita = ReplicatedVar(1, self.replicator, 'cont_partita')
        self.turno = ReplicatedVar(0, self.replicator, 'turno')
        self.fase_gioco = ReplicatedVar(ATTESA_GIOCATORI, self.replicator, 'fase_gioco')
        self.lista_player = []  # tecnicamente ognuno si fa la sua e non è replicata ma tutti mettono gli stessi valori
        # per ogni giocatore quindi è come se lo fosse
        self.add_giocatori()

    def add_giocatori(self):
        for i in range(4):
            self.lista_player.append(PlayerPublic(self, len(self.lista_player)))  # la prima volta index = 0
