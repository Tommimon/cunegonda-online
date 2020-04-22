# testo in linea semplice in cui posso specificare testo e sfondo

import pygame as pg
from client.color import NERO, BIANCO

FONT = 'freesansbold.ttf'


class Text:
    def __init__(self, text, pos, size=32, text_color=NERO, bg_color=BIANCO, bold=True):
        self._pos = pos
        self._text = text
        self._text_color = text_color
        self._bg_color = bg_color
        self.bold = bold
        self.visible = True
        self.font = pg.font.Font(FONT, size)
        self.surface = None
        self._refresh()

    def _refresh(self):  # ogni volta che cambio qualcosa devo richiamarlo
        self.surface = self.font.render(self._text, self.bold, self._text_color, self._bg_color)

    def blit(self, screen):
        if self.visible:
            screen.blit(self.surface, self._pos)

    def set_text(self, text):
        self._text = text
        self._refresh()

    def set_text_color(self, text_color):
        self._text_color = text_color
        self._refresh()

    def set_bg_color(self, bg_color):
        self._bg_color = bg_color
        self._refresh()

    def set_pos(self, pos):
        self._pos = pos
        self._refresh()

    def center(self, w_perc):  # modifico la pos orizzontale per centrare il testo
        width = self.surface.get_width()
        self.set_pos((50*w_perc - width/2, self._pos[1]))
