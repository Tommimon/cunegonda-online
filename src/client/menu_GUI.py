#  gestisce i bottoni e risolve i mouse button event

from client.color import *
from client.button import Button
from client.text import Text
from client.global_var import GlobalVar
import pygame as pg


class MenuGUI:
    def __init__(self):
        GlobalVar.player_HUD = self
        self.screen = GlobalVar.screen  # mi salvo una ref allo screen
        width, height = self.screen.get_size()
        self.w_perc = width / 100  # mi salvo misure percentuali dello schermo
        self.h_perc = height / 100
        self.titolo = Text('Main Menu', (50 * self.w_perc, 10 * self.h_perc), bg_color=ROSSO, text_color=VERDE, center=True)
        self.btn_quit = Button('Quit', (50 * self.w_perc, 80 * self.h_perc), GlobalVar.player_controller.quit,
                               bg_color=VERDE, text_color=NERO, center=True)
        self.btn_connect = Button('Connect', (50 * self.w_perc, 20 * self.h_perc), MenuGUI.switch_to_game,
                                  bg_color=VERDE, text_color=NERO, center=True)

    def display(self):
        self.screen.fill(ROSSO)  # copro frame prec
        self.titolo.blit(self.screen)
        self.btn_quit.blit(self.screen)
        self.btn_connect.blit(self.screen)
        pg.display.update()  # Or pg.display.flip()

    def mouse_click(self, pos):
        self.btn_quit.check_click(pos)
        self.btn_connect.check_click(pos)

    @staticmethod
    def switch_to_game():  # imposta game come next schermata e chiude il menu
        GlobalVar.game_instance.next_schermata = 'game'
        GlobalVar.player_controller.quit()
