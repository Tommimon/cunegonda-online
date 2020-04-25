# gestisce tutta lagui del gioco: carte, bottoni e altro

from client.color import *
from client.card_GUI import CardGUI, Card
from client.button import Button
from client.text import Text
from client.global_var import GlobalVar
from replicated.game_state import Fase
from pathlib import Path
import pygame as pg


VUOTO = Card()  # corrisponde a carta vuota
PADDING_PERC = 2  # percentuale rispetto all'altezza, distanza tra le carte


class GameGUI:
    def __init__(self):
        GlobalVar.player_HUD = self
        self.screen = GlobalVar.screen  # mi salvo una ref allo screen
        width, height = self.screen.get_size()
        self.w_p = width / 100  # mi salvo misure percentuali dello schermo
        self.h_p = height / 100
        self.dim_card = (int(12.75 * self.h_p), int(18.75 * self.h_p))
        self.top_text = Text('', (20 * self.w_p, 0), text_color=BIANCO, bg_color=NERO)
        self.text_partita = Text('', (80 * self.w_p, 0), text_color=BIANCO, bg_color=NERO)
        self.sfondo = GameGUI.init_sfondo((width, height))  # note the tuple

        self.username_sinistra = Text('', (13 * self.w_p, 28 * self.h_p), text_color=VERDE, bg_color=ROSSO, center=True)
        self.username_alto = Text('', (50 * self.w_p, 11 * self.h_p), text_color=VERDE, bg_color=ROSSO, center=True)
        self.username_destra = Text('', (87 * self.w_p, 28 * self.h_p), text_color=VERDE, bg_color=ROSSO, center=True)
        self.punteggio_sinistra = Text('', (13 * self.w_p, 21 * self.h_p), 48, ROSSO, NERO_TRASP, center=True)
        self.punteggio_alto = Text('', (50 * self.w_p, 4 * self.h_p), 48, ROSSO, NERO_TRASP, center=True)
        self.punteggio_destra = Text('', (87 * self.w_p, 21 * self.h_p), 48, ROSSO, NERO_TRASP, center=True)
        self.carta_sinistra = CardGUI(VUOTO, (13 * self.w_p, 40 * self.h_p), self.dim_card, active=False, center=True)
        self.carta_alto = CardGUI(VUOTO, (50 * self.w_p, 20 * self.h_p), self.dim_card, active=False, center=True)
        self.carta_destra = CardGUI(VUOTO, (87 * self.w_p, 40 * self.h_p), self.dim_card, active=False, center=True)

        self.text_punteggio = Text('', (0, 75 * self.h_p), text_color=ROSSO, bg_color=NERO_TRASP)
        self.punt_calcolato = True  # durante il passaggio_carte metto True a fine partita calcolo e metto False
        self.punteggio_mio = 0
        self.storico = []
        self.carta_basso = CardGUI(VUOTO, (50 * self.w_p, 55 * self.h_p), self.dim_card, active=False, center=True)
        self.gui_carte_mano = []
        self.lista_mano = []
        self.btn_indietro = Button('<', (0, 0), GlobalVar.player_controller.indietro, text_color=ROSSO, bg_color=VERDE)

    @staticmethod
    def init_sfondo(dim):
        path = Path('./res/tavolo.jpg')
        sfondo = pg.image.load(str(path))
        sfondo = pg.transform.scale(sfondo, dim)
        return sfondo

    def refresh_top(self):  # in base alla fase chiama tutte le cose da aggiornare
        n_partita = GlobalVar.game_state.cont_partita.val
        self.text_partita.set_text('Game ' + str(n_partita))
        fase = GlobalVar.game_state.fase_gioco.val
        if fase == Fase.ATTESA_GIOCATORI:  # testo top
            self.top_text.set_text('Waiting for players...')
        elif fase == Fase.PASSAGGIO_CARTE:
            self.top_text.set_text('Choose the cards to pass')
        elif fase == Fase.GIOCO:
            self.refresh_turno()

    def calcola_storico(self):
        index = GlobalVar.player_state.index.val  # prendo l'index di questo stesso giocatore
        lista_player = GlobalVar.game_state.lista_player  # prendo la lista dei giocatori del game_state
        fase = GlobalVar.game_state.fase_gioco.val
        if fase == Fase.FINE_PARTITA and not self.punt_calcolato:
            self.punt_calcolato = True  # poi in passaggio_carte viene rimesso a False
            punti = lista_player[index].punteggio_tot.val  # prendo il punteggio_tot dal game_state
            delta = punti - self.punteggio_mio
            self.punteggio_mio = punti  # aggiorno
            self.storico.append(delta)  # aggiungo punti fatti in questa allo storico
            self.top_text.set_text('You get ' + str(delta) + ' points for this game')
        elif fase == Fase.PASSAGGIO_CARTE:
            self.punt_calcolato = False  # a fine partita viene calcolato e messo true fino alla prox passaggio_carte

    def refresh_mio_punteggio(self):
        self.calcola_storico()
        stringa_punteggio = str(self.punteggio_mio) + ': '  # per mio punteggio
        for i in range(len(self.storico)):
            if i != 0:  # se non è primo
                stringa_punteggio += '/ '
            stringa_punteggio += str(self.storico[i]) + ' '  # aggiungo pezzo allo storico
        self.text_punteggio.set_text(stringa_punteggio)

    def refresh_punteggi(self):
        index = GlobalVar.player_state.index.val  # prendo l'index di questo stesso giocatore
        lista_player = GlobalVar.game_state.lista_player  # prendo la lista dei giocatori del game_state
        self.refresh_mio_punteggio()
        self.punteggio_sinistra.set_text(str(lista_player[(index + 1) % 4].punteggio_tot.val))  # per altri
        self.punteggio_alto.set_text(str(lista_player[(index + 2) % 4].punteggio_tot.val))
        self.punteggio_destra.set_text(str(lista_player[(index + 3) % 4].punteggio_tot.val))

    def refresh_usernames(self):
        index = GlobalVar.player_state.index.val  # prendo l'index di questo stesso giocatore
        lista_player = GlobalVar.game_state.lista_player  # prendo la lista dei giocatori del game_state
        self.username_sinistra.set_text(lista_player[(index + 1) % 4].username.val)
        self.username_alto.set_text(lista_player[(index + 2) % 4].username.val)
        self.username_destra.set_text(lista_player[(index + 3) % 4].username.val)

    def refresh_turno(self):
        turno = GlobalVar.game_state.turno.val  # prendo il numero del turno
        if turno == GlobalVar.player_state.index.val:  # se tocca a questo stesso giocatore
            self.top_text.set_text('Your turn')
        else:
            username = GlobalVar.game_state.lista_player[turno].username.val  # prendo il nome di chi deve giocare
            self.top_text.set_text(username + "'s turn")  # scrivo a chi tocca

    def refresh_carte(self):
        index = GlobalVar.player_state.index.val  # prendo l'index di questo stesso giocatore
        lista_player = GlobalVar.game_state.lista_player  # prendo la lista dei giocatori del game_state
        self.carta_basso.set_carta(lista_player[index].carta_giocata.val)
        self.carta_sinistra.set_carta(lista_player[(index + 1) % 4].carta_giocata.val)
        self.carta_alto.set_carta(lista_player[(index + 2) % 4].carta_giocata.val)
        self.carta_destra.set_carta(lista_player[(index + 3) % 4].carta_giocata.val)
        new_mano = GlobalVar.player_state.mano.val.copy()
        if new_mano != self.lista_mano:
            self.lista_mano = new_mano
            self.gui_carte_mano = []
            self.refresh_mano()

    def refresh_mano(self):
        padding = PADDING_PERC * self.h_p
        x = padding * 2
        delta = self.dim_card[0] + padding
        mano_ordinata = Card.sort_carte(self.lista_mano)
        for carta in mano_ordinata:
            self.gui_carte_mano.append(CardGUI(carta, (x, 80 * self.h_p), self.dim_card))
            x += delta

    def display(self):  # chiama tutte le cose da blittare
        self.screen.fill(NERO)  # copro frame prec
        self.screen.blit(self.sfondo, (0, 0))
        self.display_top()
        fase = GlobalVar.game_state.fase_gioco.val
        if fase != Fase.ATTESA_GIOCATORI:
            self.display_usernames()
            self.display_punteggi()
        if fase == Fase.PASSAGGIO_CARTE or fase == Fase.GIOCO:
            self.display_carte()
        pg.display.update()  # Or pg.display.flip()

    def display_top(self):
        self.refresh_top()
        self.btn_indietro.blit(self.screen)
        self.top_text.blit(self.screen)
        self.text_partita.blit(self.screen)

    def display_usernames(self):
        self.refresh_usernames()
        self.username_sinistra.blit(self.screen)
        self.username_alto.blit(self.screen)
        self.username_destra.blit(self.screen)

    def display_punteggi(self):
        self.refresh_punteggi()
        self.punteggio_sinistra.blit(self.screen)
        self.punteggio_alto.blit(self.screen)
        self.punteggio_destra.blit(self.screen)
        self.text_punteggio.blit(self.screen)

    def display_carte(self):
        self.refresh_carte()
        self.carta_basso.blit(self.screen)
        self.carta_sinistra.blit(self.screen)
        self.carta_alto.blit(self.screen)
        self.carta_destra.blit(self.screen)
        for c in self.gui_carte_mano:
            c.blit(self.screen)

    def mouse_click(self, pos):
        self.btn_indietro.check_click(pos)
        for carta in self.gui_carte_mano:
            carta.check_click(pos)

    @staticmethod
    def gioca_la_prima():
        GlobalVar.player_controller.gioca_carta(GlobalVar.player_state.mano[0])
        # non richiamo il metodo dalla classe anche se statico perché non posso importare qui PlayerController per
        # evitare import circolari
