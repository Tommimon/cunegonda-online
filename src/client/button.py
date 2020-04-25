# come bottoni uso dei testi in cui implemento la possibilità di cliccare

from client.text import Text
from client.color import NERO, BIANCO


class Button(Text):
    def __init__(self, text, pos, action, size=32, text_color=NERO, bg_color=BIANCO, bold=True, center=False):
        super().__init__(text, pos, size, text_color, bg_color, bold, center)
        self.action = action  # questa deve essere una funzione, viene eseguita quando clicco il bottone
        self.activated = True
        self.rect = None
        self._refresh()

    def _refresh(self):  # ogni volta che cambio qualcosa devo richiamarlo
        super()._refresh()  # eredo il refresh che riguarda il testo
        self.rect = self.surface.get_rect()  # aggiorno il rect che identifica la parte cliccabile
        self.rect.topleft = self.center_pos()

    def check_click(self, mouse_pos):
        if self.activated:
            if self.rect.collidepoint(mouse_pos):
                self.action()
