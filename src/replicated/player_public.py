# mette insieme le variabili di uno stesso giocatore usate dal game_state

from card import *
from comunication import *


class PlayerPublic:
    def __init__(self, game_state, index):
        self.game_state = game_state
        self.index = index
        self.username = ''
        self.punteggio_tot = 0
        self.carta_giocata = Card()

    def _replicate_var(self, nome_var, valore):  # si occupa di dire a tutti il cambiamento
        mess = Messaggio()
        mess.tipo = PLAYER_PUBLIC_TYPE
        mess.add_campo_int('index', self.index)
        mess.add_campo('nome_variabile', nome_var)
        mess.add_campo(nome_var, valore)
        self.game_state.send_all(mess)

    def _replicate_var_int(self, nome_var, valore):
        mess = Messaggio()
        mess.tipo = PLAYER_PUBLIC_TYPE
        mess.add_campo_int('index', self.index)
        mess.add_campo('nome_variabile', nome_var)
        mess.add_campo_int(nome_var, valore)
        self.game_state.send_all(mess)

    def _replicate_var_card(self, nome_carta, seme, valore):
        mess = Messaggio()
        mess.tipo = PLAYER_PUBLIC_TYPE
        mess.add_campo_int('index', self.index)
        mess.add_campo('nome_variabile', nome_carta)
        mess.add_campo_int('seme', seme)
        mess.add_campo_int('valore', valore)
        self.game_state.send_all(mess)

    def set_rep_username(self, username):  # va chiamato solo lato server
        self.username = username
        self._replicate_var('username', username)

    def set_rep_punteggio_tot(self, punteggio):
        self.punteggio_tot = punteggio
        self._replicate_var_int('punteggio_tot', punteggio)

    def set_rep_carta_gioc(self, carta):
        self.carta_giocata = carta
        self._replicate_var_card('carta_giocata', carta.seme, carta.valore)

    def risolvi_messaggio(self, messaggio):  # legge i messaggi del server sul lato client
        nome_var = messaggio.get_campo('nome_variabile')
        if nome_var == 'username':
            self.username = messaggio.get_campo(nome_var)  # ovviamente nome_var è 'username'
            print('set user', self.username)
        elif nome_var == 'punteggio_tot':
            self.punteggio_tot = messaggio.get_campo_int(nome_var)
            print('set punteggio_tot', self.punteggio_tot)
        elif nome_var == 'carta_giocata':
            # ricompongo la carta dal messaggio
            self.carta_giocata = Card(messaggio.get_campo_int('valore'), messaggio.get_campo_int('seme'))
            print('set carta_giocata', self.carta_giocata.seme, self.carta_giocata.valore)
