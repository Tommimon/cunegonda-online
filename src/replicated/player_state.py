# contiene solo i dati condivisi tra owner client e server
from tcp_basics import Replicator, ReplicatedVar
from card import Card

try:
    import server.global_var as server_gv  # solo per lato server
except ImportError:  # sul client non posso importarlo ma tanto non serve
    server_gv = None  # se scrivo così non mi da una warning (ma tanto in teoria non lo dovrei usare se arrivo qui)

try:
    import client.global_var as client_gv  # in teori se siamo arrivati qui è client e non da errori
except ImportError:
    client_gv = None


class PlayerState:
    def __init__(self, auth=False, index=None):
        # devo preoccuparmi di avere un id_rep diverso per ogni player state lato server
        if auth:  # significa se è server
            id_rep = 'player_state' + str(index)
        else:
            id_rep = 'player_state*'  # asterisco è il carattere jolly perché non so ancora il mio index
        self.replicator = Replicator(id_rep, auth=auth)
        # solo per l'username l'auth è al contrario perché è il client a decidere il suo username qui
        self.username = ReplicatedVar(None, self.replicator, 'username', auth=(not self.replicator.auth),
                                      on_rep=self.richiesta_username)
        self.index = ReplicatedVar(index, self.replicator, 'index', on_rep=self.recive_index)  # serve solo a client
        if auth:
            self.index.rep_val()  # perché il valore iniziale non si replica in automatico
        self.param_ceck = ReplicatedVar(0, self.replicator, 'param_ceck', auth=(not self.replicator.auth),
                                        on_rep=self.recv_ceck)
        self.mano = ReplicatedVar([], self.replicator, 'mano')
        # param_scelta come altre è una var fittizia usata solo come parametro per la funzione di on_rep questo serve
        # per poter eseguire la funzione dal lato di chi riceve la var anche se di fatto l'ho chiamata dall'altro lato
        self.param_scelta = ReplicatedVar(Card(), self.replicator, 'param_scelta', auth=(not self.replicator.auth),
                                          on_rep=self.richiesta_carta_scelta)
        self.scambiate = ReplicatedVar([], self.replicator, 'scambiate')

    def recive_index(self):  # eseguito da client
        self.replicator.id = 'player_state' + str(self.index.val)
        self.username.val = client_gv.GlobalVar.game_instance.username

    def recv_ceck(self):  # su server
        private = server_gv.GlobalVar.game_mode.lista_player[self.index.val]  # trovo il private per index
        private.reset_timer()

    def richiesta_username(self):  # eseguito da server
        try:
            stringa = str(self.username.val)
            server_gv.GlobalVar.game_state.lista_player[self.index.val].username.val = stringa
            # gli do il valore che è appena arrivato ed è stato appena settato in self.username.val
            print('set username', stringa)
        except:  # così sono sicuro che uno non possa far crashare il server da fuori
            pass

    def richiesta_carta_scelta(self):  # eseguito su server a differenza degli altri tre
        if server_gv.GlobalVar.game_mode.tutti_connessi:  # se no la richiesta viene ignorata e va persa
            if type(self.param_scelta.val) == Card:  # mi accerto che il valore sia una carta per evitare errori
                server_gv.GlobalVar.game_mode.carta_client(self.index.val, self.param_scelta.val)
                # la gamemode si occupa di eseguire l'azione
