# mette insieme le variabili di uno stesso giocatore usate dalla gamemode (privati del server)

from replicated.player_state import PlayerState
from threading import Timer
from server.global_var import GlobalVar

CONNECTION_TIMEOUT = 5


class PlayerPrivate:
    def __init__(self, socket, index):
        self.socket = socket  # serve alla gamemode
        self.punteggio = 0
        self.carte_prese = []
        self.player_state = PlayerState(auth=True, index=index)
        # nota che dentro al player state le var sono pubbliche
        self.timer = Timer(CONNECTION_TIMEOUT, self.disconnetti)
        self.timer.start()

    def reset_timer(self):
        self.timer.cancel()
        self.timer = Timer(CONNECTION_TIMEOUT, self.disconnetti)
        self.timer.start()

    def disconnetti(self):
        GlobalVar.game_mode.disconnetti(self)
        print('disconnected', self.player_state.index.val)
