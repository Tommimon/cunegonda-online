#  gestisce i bottoni e risolve i mouse button event

from client.button import *
from client.global_var import *


class MenuHUD:
    def __init__(self):
        GlobalVar.player_HUD = self
        self.screen = GlobalVar.screen  # mi salvo una ref allo screen
        width, height = self.screen.get_size()
        self.w_perc = width / 100  # mi salvo misure percentuali dello schermo
        self.h_perc = height / 100
        self.titolo = Text('Main Menu', (0, 10 * self.h_perc), bg_color=NERO, text_color=BIANCO)
        self.btn_quit = Button('Quit', (0, 80 * self.h_perc), GlobalVar.player_controller.quit,
                               bg_color=ROSSO, text_color=BIANCO)
        self.btn_connect = Button('Connect', (0, 20 * self.h_perc), MenuHUD.switch_to_game,
                                  bg_color=VERDE, text_color=BIANCO)
        self.centra_menu()

    def centra_menu(self):  # semplicemente mette al centro tutti gli elementi, ho fatto metodo apposito per fare ordine
        self.titolo.center(self.w_perc)
        self.btn_quit.center(self.w_perc)
        self.btn_connect.center(self.w_perc)

    def display(self):
        self.screen.fill(NERO)  # copro frame prec
        self.titolo.blit(self.screen)
        self.btn_quit.blit(self.screen)
        self.btn_connect.blit(self.screen)
        pg.display.update()  # Or pg.display.flip()

    def mouse_click(self, pos):
        self.btn_quit.ceck_click(pos)
        self.btn_connect.ceck_click(pos)

    @staticmethod
    def switch_to_game():  # imposta game come next schermata e chiude il menu
        GlobalVar.game_instance.next_schermata = 'game'
        GlobalVar.player_controller.quit()
