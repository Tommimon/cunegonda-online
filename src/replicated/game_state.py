# contiene i dati pubblici per tutti

from replicated.player_public import *

# FASI
ATTESA_GIOCATORI = 1
PASSAGGIO_CARTE = 2
GIOCO = 3
FINE_PARTITA = 4


class GameState:
    def __init__(self):
        self.lista_socket = []  # usato solo lato server
        self.cont_partita = 1
        self.turno = 0
        self.fase_gioco = ATTESA_GIOCATORI
        self.lista_player = []  # tecnicamente ognuno si fa la sua e non è replicata ma tutti mettono gli stessi valori
        # per ogni giocatore quindi è come se lo fosse
        self.add_giocatori()

    def add_giocatori(self):
        for i in range(4):
            self.lista_player.append(PlayerPublic(self, len(self.lista_player)))  # la prima volta index = 0

    def send_all(self, messaggio):
        for socket in self.lista_socket:
            messaggio.safe_send(socket)

    def _replicate_var_int(self, nome_var, valore):
        mess = Messaggio()
        mess.tipo = GAME_TYPE
        mess.add_campo('nome_variabile', nome_var)
        mess.add_campo_int(nome_var, valore)
        self.send_all(mess)

    def set_rep_cont_partita(self, cont):
        self.cont_partita = cont
        self._replicate_var_int('cont_partita', cont)

    def set_rep_turno(self, turno):
        self.turno = turno
        self._replicate_var_int('turno', turno)

    def set_rep_fase(self, fase):
        self.fase_gioco = fase
        self._replicate_var_int('fase_gioco', fase)

    def risolvi_messaggio(self, messaggio):  # legge i messaggi del server sul lato client
        nome_var = messaggio.get_campo('nome_variabile')
        if nome_var == 'cont_partita':
            self.cont_partita = messaggio.get_campo_int(nome_var)
            print('set n_partita', self.cont_partita)
        elif nome_var == 'turno':
            self.turno = messaggio.get_campo_int(nome_var)
            print('set turno', self.turno)
        elif nome_var == 'fase_gioco':
            self.fase_gioco = messaggio.get_campo_int(nome_var)
            print('set fase', self.fase_gioco)
