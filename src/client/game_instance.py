# resposabile delle variabili che persistono tra diverse schermate e del passaggio tra di esse

from settings_reader import SettingsReader
from client.menu_controller import MenuController
from client.game_controller import GameController
from replicated.game_state import GameState
from replicated.player_state import PlayerState
from client.global_var import GlobalVar
import pygame as pg


# PARAMETRI
SETTINGS_FILE = 'client_settings.txt'

# RISOLUZIONE
# in resizable 4/5
# in fullscreen 5/6


class GameInstance:
    def __init__(self):
        GlobalVar.game_instance = self
        settings = SettingsReader(SETTINGS_FILE)  # leggo le impostazioni da file
        self.username = settings.get_val('username')
        self.server_address = (settings.get_val('server_ip'), int(settings.get_val('server_port')))
        self.res = (int(settings.get_val('resolution_x')), int(settings.get_val('resolution_y')))
        self.crea_screen()
        self.next_schermata = None  # se c'è è una stringa con il nome dello schermo

    def crea_screen(self):
        succes, fail = pg.init()
        print('pygame init error:', fail)
        GlobalVar.screen = pg.display.set_mode(self.res, pg.FULLSCREEN)  # creo lo schermo
        # GlobalVar.screen = pg.display.set_mode((1500, 750))  # for debug
        pg.display.set_caption('Cunegonda')

    def gestisci_schermate(self):  # regola il passaggio tra le varie schermate
        while self.next_schermata is not None:  # se non c'è quitto
            nome = self.next_schermata
            self.next_schermata = None  # svuoto next schermata
            if nome == 'menu':
                GameInstance.menu()
            elif nome == 'game':
                GameInstance.game()

    @staticmethod
    def menu():  # crea i componenti principali per il menu
        print('opening menu...')
        controller = MenuController()  # si mette da solo in GlobalVar
        controller.loop()

    @staticmethod
    def game():  # crea i componenti principali per il gioco
        print('opening game...')
        GlobalVar.game_state = GameState(auth=False)
        GlobalVar.player_state = PlayerState(auth=False)
        controller = GameController()
        controller.loop()
