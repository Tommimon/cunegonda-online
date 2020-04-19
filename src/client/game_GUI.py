# gestisce tutta lagui del gioco: carte, bottoni e altro

from client.card_GUI import *
from client.button import *
from client.global_var import *
from replicated.game_state import *


VUOTO = Card(Card.NESSUN_SEME, Card.NESSUN_VALORE)


class GameHUD:
    def __init__(self):
        GlobalVar.player_HUD = self
        self.screen = GlobalVar.screen  # mi salvo una ref allo screen
        width, height = self.screen.get_size()
        self.w_perc = width / 100  # mi salvo misure percentuali dello schermo
        self.h_perc = height / 100
        self.top_text = Text('', (20 * self.w_perc, 0), text_color=BIANCO, bg_color=NERO)
        self.text_partita = Text('', (80 * self.w_perc, 0), text_color=BIANCO, bg_color=NERO)

        self.username_sinistra = Text('', (0, 30 * self.h_perc), text_color=BLU, bg_color=NERO)
        self.username_alto = Text('', (40 * self.w_perc, 10 * self.h_perc), text_color=BLU, bg_color=NERO)
        self.username_destra = Text('', (80 * self.w_perc, 30 * self.h_perc), text_color=BLU, bg_color=NERO)
        self.punteggio_sinistra = Text('', (0, 25 * self.h_perc), text_color=ROSSO, bg_color=NERO)
        self.punteggio_alto = Text('', (40 * self.w_perc, 5 * self.h_perc), text_color=ROSSO, bg_color=NERO)
        self.punteggio_destra = Text('', (80 * self.w_perc, 25 * self.h_perc), text_color=ROSSO, bg_color=NERO)
        self.carta_sinistra = CardHUD(VUOTO, (0, 40 * self.h_perc), (68, 100), activated=False)
        self.carta_alto = CardHUD(VUOTO, (40 * self.w_perc, 20 * self.h_perc), (68, 100), activated=False)
        self.carta_destra = CardHUD(VUOTO, (80 * self.w_perc, 40 * self.h_perc), (68, 100), activated=False)

        self.text_punteggio = Text('', (0, 70 * self.h_perc), text_color=VERDE, bg_color=NERO)
        self.punt_calcolato = True  # durante il passaggio_carte metto True a fine partita calcolo e metto False
        self.punteggio_mio = 0
        self.storico = []
        self.carta_basso = CardHUD(VUOTO, (40 * self.w_perc, 50 * self.h_perc), (68, 100), activated=False)
        self.lista_carte_mano = []
        self.lista_mano = []
        self.btn_indietro = Button('<--', (0, 0), GlobalVar.player_controller.indietro, text_color=BIANCO, bg_color=BLU)

    def refresh(self):
        n_partita = GlobalVar.game_state.cont_partita
        self.text_partita.set_text('Game ' + str(n_partita))
        fase = GlobalVar.game_state.fase_gioco
        if fase == ATTESA_GIOCATORI:  # testo top
            self.top_text.set_text('In attesa di altri giocatori')
        elif fase == PASSAGGIO_CARTE:
            self.punt_calcolato = False  # a fine partita viene calcolato e messo true fino alla prox passaggio_carte
            self.top_text.set_text('Seleziona le carte da passare')
        elif fase == GIOCO:
            turno = GlobalVar.game_state.turno  # prendo il numero del turno
            if turno == GlobalVar.player_state.index:  # se tocca a questo stesso giocatore
                self.top_text.set_text('Tocca a te')
            else:
                username = GlobalVar.game_state.lista_player[turno].username  # prendo il nome di chi deve giocare
                self.top_text.set_text('Tocca a ' + username)  # scrivo a chi tocca

        if fase != ATTESA_GIOCATORI:
            index = GlobalVar.player_state.index  # prendo l'index di questo stesso giocatore
            lista_player = GlobalVar.game_state.lista_player  # prendo la lista dei giocatori del game_state
            if fase == FINE_PARTITA and not self.punt_calcolato:
                self.punt_calcolato = True  # poi in passaggio_carte viene rimesso a False
                punti = lista_player[index].punteggio_tot  # prendo il punteggio_tot dal game_state
                delta = punti - self.punteggio_mio
                self.punteggio_mio = punti  # aggiorno
                self.storico.append(delta)  # aggiungo punti fatti in questa allo storico
                self.top_text.set_text('Hai fatto ' + str(delta) + ' punti in questa partita')
            stringa_punteggio = str(self.punteggio_mio) + ': '  # per mio punteggio
            for i in range(len(self.storico)):
                if i != 0:  # se non è primo
                    stringa_punteggio += '/ '
                stringa_punteggio += str(self.storico[i]) + ' '  # aggiungo pezzo allo storico
            self.text_punteggio.set_text(stringa_punteggio)
            self.punteggio_sinistra.set_text(str(lista_player[(index + 1) % 4].punteggio_tot))  # per altri
            self.punteggio_alto.set_text(str(lista_player[(index + 2) % 4].punteggio_tot))
            self.punteggio_destra.set_text(str(lista_player[(index + 3) % 4].punteggio_tot))
            self.username_sinistra.set_text(lista_player[(index + 1) % 4].username)
            self.username_alto.set_text(lista_player[(index + 2) % 4].username)
            self.username_destra.set_text(lista_player[(index + 3) % 4].username)

    def display(self):
        self.refresh()
        self.screen.fill(NERO)  # copro frame prec
        self.top_text.blit(self.screen)
        self.text_partita.blit(self.screen)
        self.username_sinistra.blit(self.screen)
        self.username_alto.blit(self.screen)
        self.username_destra.blit(self.screen)
        self.btn_indietro.blit(self.screen)
        fase = GlobalVar.game_state.fase_gioco
        if fase != ATTESA_GIOCATORI:
            self.punteggio_sinistra.blit(self.screen)
            self.punteggio_alto.blit(self.screen)
            self.punteggio_destra.blit(self.screen)
            self.text_punteggio.blit(self.screen)
        if fase == PASSAGGIO_CARTE or fase == GIOCO:
            self.display_carte()
        pg.display.update()  # Or pg.display.flip()

    def refresh_mano(self):
        x = 30
        for carta in self.lista_mano:
            self.lista_carte_mano.append(CardHUD(carta, (x, 80 * self.h_perc), (68, 100)))
            x += 78

    def refresh_carte(self):
        index = GlobalVar.player_state.index  # prendo l'index di questo stesso giocatore
        lista_player = GlobalVar.game_state.lista_player  # prendo la lista dei giocatori del game_state
        self.carta_basso.set_carta(lista_player[index].carta_giocata)
        self.carta_sinistra.set_carta(lista_player[(index + 1) % 4].carta_giocata)
        self.carta_alto.set_carta(lista_player[(index + 2) % 4].carta_giocata)
        self.carta_destra.set_carta(lista_player[(index + 3) % 4].carta_giocata)
        new_mano = GlobalVar.player_state.mano.copy()
        if new_mano != self.lista_mano:
            self.lista_mano = new_mano
            self.lista_carte_mano = []
            self.refresh_mano()

    def display_carte(self):
        self.refresh_carte()
        self.carta_basso.blit(self.screen)
        self.carta_sinistra.blit(self.screen)
        self.carta_alto.blit(self.screen)
        self.carta_destra.blit(self.screen)
        for c in self.lista_carte_mano:
            c.blit(self.screen)

    def mouse_click(self, pos):
        self.btn_indietro.check_click(pos)
        for carta in self.lista_carte_mano:
            carta.check_click(pos)

    @staticmethod
    def gioca_la_prima():
        GlobalVar.player_controller.gioca_carta(GlobalVar.player_state.mano[0])
