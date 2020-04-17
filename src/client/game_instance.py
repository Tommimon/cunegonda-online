# resposabile delle variabili che persistono tra diverse schermate e del passaggio tra di esse

from settings_reader import *
from client.menu_controller import *
from client.game_controller import *
from replicated.game_state import *
from replicated.player_state import *


# PARAMETRI
SETTINGS_FILE = 'client_settings.txt'
RISOLUZIONE = (1080, 720)


class GameInstance:
    def __init__(self):
        GlobalVar.game_instance = self
        settings = SettingsReader(SETTINGS_FILE)  # leggo le impostazioni da file
        self.username = settings.get_val('username')
        self.server_address = (settings.get_val('server_ip'), int(settings.get_val('server_port')))
        GameInstance.crea_screen()
        self.next_schermata = None  # se c'è è una stringa con il nome dello schermo

    @staticmethod
    def crea_screen():
        succes, fail = pg.init()
        print('pygame init error:', fail)
        GlobalVar.screen = pg.display.set_mode(RISOLUZIONE)  # mostro schermo
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
    def menu():
        print('opening menu...')
        controller = MenuController()  # si mette da solo in GlobalVar
        controller.loop()

    @staticmethod
    def game():
        print('opening game...')
        GlobalVar.game_state = GameState()
        GlobalVar.player_state = PlayerState()
        controller = GameController()
        controller.loop()
