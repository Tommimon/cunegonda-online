# mette insieme le variabili di uno stesso giocatore usate dalla gamemode (privati del server)

from replicated.player_state import PlayerState


class PlayerPrivate:
    def __init__(self, socket, index):
        self.socket = socket  # serve alla gamemode
        self.punteggio = 0
        self.carte_prese = []
        self.player_state = PlayerState(auth=True, index=index)
        # nota che dentro al player state le var sono pubbliche
