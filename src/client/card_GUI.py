#  crea il rettangolo cliccabile della carta in cui compare l'immagine

import pygame as pg
from card import *
from client.global_var import *
from pathlib import Path


class CardGUI:
    def __init__(self, carta, pos, dim, activated=True):
        self._pos = pos
        self.dim = dim
        self._carta = None
        self.vuoto = None
        self._immagine = None
        self.rect = None
        self.set_carta(carta)
        self.visible = True
        self.activated = activated

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
                self.rect.topleft = self._pos

    def blit(self, screen):
        if self.visible and not self.vuoto:
            screen.blit(self._immagine, self._pos)

    def check_click(self, mouse_pos):
        if self.activated and not self.vuoto:
            if self.rect.collidepoint(mouse_pos):
                GlobalVar.player_controller.gioca_carta(self._carta)


