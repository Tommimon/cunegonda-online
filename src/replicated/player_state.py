# contiene solo i dati condivisi tra owner client e server
from tcp_basics import Replicator, ReplicatedVar
from comunication import *
from card import *


class PlayerState:
    def __init__(self, socket=None, auth=False):
        self.replicator = Replicator('player_state', auth=auth)
        self.index = ReplicatedVar(None, self.replicator, 'index')  # utile solo al client perché il server li ha in ordine
        self.mano = []
        self.scambiate = []
        self.socket = socket  # usato solo lato server

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
