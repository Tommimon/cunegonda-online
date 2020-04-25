#  crea il rettangolo cliccabile della carta in cui compare l'immagine

import pygame as pg
from pathlib import Path
from card import Card
from client.global_var import GlobalVar
from replicated.game_state import Fase


class CardGUI:
    def __init__(self, carta, pos, dim, active=True, center=False):
        self._pos = pos
        self.dim = dim
        self._carta = None
        self.vuoto = None
        self._immagine = None
        self.rect = None
        self.center = center
        self.set_carta(carta)
        self.visible = True
        self.active = active
        self.evidenziatore = self.get_evidenziatore()

    def get_evidenziatore(self):
        path = Path('./res/evidenziatore.png')
        evidenz = pg.image.load(str(path))
        return pg.transform.scale(evidenz, (int(self.dim[0] * 1.118), int(self.dim[1] * 1.118)))

    def nome_carta(self):  # restituisce nome file es: valore_seme.jpeg
        if self._carta.valore < 11:  # se è un numero
            stringa_val = str(self._carta.valore)
        elif self._carta.valore == Card.JACK:
            stringa_val = 'jack'
        elif self._carta.valore == Card.DONNA:
            stringa_val = 'donna'
        elif self._carta.valore == Card.RE:
            stringa_val = 're'
        elif self._carta.valore == Card.ASSO:
            stringa_val = 'asso'

        if self._carta.seme == Card.CUORI:
            stringa_seme = 'cuori'
        elif self._carta.seme == Card.QUADRI:
            stringa_seme = 'quadri'
        elif self._carta.seme == Card.FIORI:
            stringa_seme = 'fiori'
        elif self._carta.seme == Card.PICCHE:
            stringa_seme = 'picche'
        return stringa_val + '_' + stringa_seme + '.png'

    def get_immagine(self):
        if not self.vuoto:
            file_name = self.nome_carta()
            path = Path('./res/') / file_name
            picture = pg.image.load(str(path))
            picture = pg.transform.scale(picture, self.dim)
            self._immagine = picture

    def set_carta(self, carta):
        if carta.valore == Card.NESSUN_VALORE and carta.seme == Card.NESSUN_SEME:
            self.vuoto = True
        else:
            self.vuoto = False
        # se la carta è cambiata o se non c'era proprio
        if self._carta is None or self._carta.valore != carta.valore or self._carta.seme != carta.seme:
            self._carta = carta
            if not self.vuoto:  # nota che se la nuova è vuota aggiorno _carta ma non immagine e rect
                self.get_immagine()
                self.rect = self._immagine.get_rect()
                self.rect.topleft = self.center_pos()

    def blit(self, screen, mostra_evidenz=False):
        if self.visible and not self.vuoto:
            seme = GlobalVar.game_state.seme_primo.val
            mano = GlobalVar.player_state.mano.val
            turno = GlobalVar.game_state.turno.val
            index = GlobalVar.player_state.index.val
            if (mostra_evidenz and Card.carta_permessa(mano, seme, self._carta) and turno == index and self.active
                    and GlobalVar.game_state.fase_gioco.val == Fase.GIOCO):
                screen.blit(self.evidenziatore, self.pos_evidenz())
            screen.blit(self._immagine, self.center_pos())

    def check_click(self, mouse_pos):
        if self.active and not self.vuoto:
            if self.rect.collidepoint(mouse_pos):
                GlobalVar.player_controller.gioca_carta(self._carta)

    def center_pos(self):  # restituisco una pos modificata per centrare il testo se sereve se no da la pos normale
        width = self.dim[0]
        if self.center:
            pos_x = self._pos[0]
            return pos_x - width / 2, self._pos[1]
        else:
            return self._pos

    def pos_evidenz(self):
        pos = self.center_pos()
        return pos[0] - self.dim[0] * 0.059, pos[1] - self.dim[1] * 0.05  # tolgo la metà della dif espressa in perc
