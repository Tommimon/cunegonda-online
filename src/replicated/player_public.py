# mette insieme le variabili di uno stesso giocatore usate dal game_state

from card import *
from tcp_basics import ReplicatedVar, Replicator


class PlayerPublic:
    def __init__(self, game_state, index):
        self.game_state = game_state
        id_player = 'player_private' + str(index)
        # bindo i socket di questo replicator a quelli del game_state
        self.replicator = Replicator(id_player, game_state.replicator.auth, game_state.replicator.sockets)
        self.index = ReplicatedVar(index, self.replicator, 'index')
        self.username = ReplicatedVar('', self.replicator, 'username')
        self.punteggio_tot = ReplicatedVar(0, self.replicator, 'punteggio_tot')
        self.carta_giocata = ReplicatedVar(Card(), self.replicator, 'carta_giocata')
