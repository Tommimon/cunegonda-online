# mette insieme le variabili di uno stesso giocatore usate dalla gamemode (privati del server)

from replicated.player_state import *


class PlayerPrivate:
    def __init__(self, socket):
        self.socket = socket  # identificativo
        self.punteggio = 0
        self.carte_prese = []
        self.player_state = PlayerState(self.socket)  # nota che dentro al player state le var sono pubbliche
