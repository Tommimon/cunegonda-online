# contiene solo i dati condivisi tra owner client e server
from tcp_basics import Replicator, ReplicatedVar
from comunication import *
from card import *

try:
    import server.global_var as server_gv  # solo per lato server
except ImportError:  # sul client non posso importarlo ma tanto non serve
    server_gv = None  # se scrivo così non mi da una warning (ma tanto in teoria non lo dovrei usare se arrivo qui)

try:
    import client.global_var as client_gv  # in teori se siamo arrivati qui è client e non da errori
except ImportError:
    client_gv = None


class PlayerState:
    def __init__(self, socket=None, auth=False, index=None):
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
        self.mano = []
        self.scambiate = []
        self.socket = socket  # usato solo lato server

    def recive_index(self):
        self.replicator.id = 'player_state' + str(self.index.val)
        self.username.val = client_gv.GlobalVar.game_instance.username

    def richiesta_username(self):
        server_gv.GlobalVar.game_state.lista_player[self.index.val].username.val = self.username.val
        # gli do il valore che è appena arrivato ed è stato appena settato in self.username.val
        print('set username', self.username.val)

    def _replicate_var_card(self, nome_var, seme, valore):  # qui non serve diere nome var perché ne ho una
        mess = Messaggio()
        mess.tipo = PLAYER_LOCAL_TYPE
        mess.add_campo('nome_variabile', nome_var)
        mess.add_campo_int('seme', seme)
        mess.add_campo_int('valore', valore)
        mess.safe_send(self.socket)

    def add_to_mano(self, carta):
        self.mano.append(carta)
        self._replicate_var_card('mano', carta.seme, carta.valore)

    def _del_from_mano(self, cercata):  # non posso usare subito remove perché è una carta distinta ma con stessi valori
        for c in self.mano:
            if c.seme == cercata.seme and c.valore == cercata.valore:  # se ha stessi valori
                self.mano.remove(c)  # lo tolgo

    def del_rep_from_mano(self, carta):
        self._del_from_mano(carta)
        self._replicate_var_card('del_mano', carta.seme, carta.valore)

    def add_to_scambiate(self, carta):
        self.scambiate.append(carta)
        self._replicate_var_card('scambiate', carta.seme, carta.valore)

    def clear_scambiate(self):
        self.scambiate = []
        self._replicate_var_int('clear_scambiate', 0)  # int perché non so che mettere

    # nota che se devo aggiungere altre var da leggere qui verrà un if, elif, elif...
    def risolvi_messaggio(self, messaggio):  # legge i messaggi del server sul lato client
        nome_var = messaggio.get_campo('nome_variabile')
        if nome_var == 'mano':
            new_carta = Card(messaggio.get_campo_int('valore'), messaggio.get_campo_int('seme'))
            self.mano.append(new_carta)
            print('new_to_mano', new_carta.seme, new_carta.valore)
        elif nome_var == 'del_mano':
            new_carta = Card(messaggio.get_campo_int('valore'), messaggio.get_campo_int('seme'))
            self._del_from_mano(new_carta)
            print('del_from_mano', new_carta.seme, new_carta.valore)
        elif nome_var == 'scambiate':
            new_carta = Card(messaggio.get_campo_int('valore'), messaggio.get_campo_int('seme'))
            self.scambiate.append(new_carta)
            print('new_to_scambiate', new_carta.seme, new_carta.valore)
        elif nome_var == 'clear_scambiate':
            self.scambiate = []
            print('clear_scambiate')
