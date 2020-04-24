# gestisce gli eventi di pygame per il gioco vero e proprio

from client.game_GUI import GameGUI
from replicated.game_state import Fase
from tcp_basics import safe_recv_var
from client.global_var import GlobalVar
from client.ceck_timer import CeckTimer
import socket as sock
import pygame as pg

FPS = 60  # Frames per second.
TIMEOUT = 0.02


class GameController:
    def __init__(self):
        GlobalVar.player_controller = self
        self.GUI = GameGUI()  # creo HUD e mi salvo una ref
        self.socket = sock.socket(sock.AF_INET, sock.SOCK_STREAM)
        self.replicators = [GlobalVar.player_state.replicator, GlobalVar.game_state.replicator]  # mi salvo tutti i...
        for g in GlobalVar.game_state.lista_player:  # replicator, nel for quelli dei player_public
            self.replicators.append(g.replicator)
        self.ceck_timer = None
        self.connettiti()
        self.clock = pg.time.Clock()  # inizializzo clock
        self.running = True

    def loop(self):
        while self.running:
            self.clock.tick(FPS)  # mi fa andare al giusto frame rate
            self.server_events()
            self.pygame_events()
            self.GUI.display()

    def pygame_events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.quit()
            if event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
                self.GUI.mouse_click(event.pos)

    def server_events(self):
        safe_recv_var(self.replicators)

    def quit(self):
        self.running = False

    def indietro(self):
        GlobalVar.game_instance.next_schermata = 'menu'
        try:
            self.ceck_timer.stop()  # se non mi connetto questo non è stato inittato
        except AttributeError:
            pass
        self.quit()

    def connettiti(self):  # se non mi connetto al server torno al menu
        try:
            self.socket.connect(GlobalVar.game_instance.server_address)
            GlobalVar.game_state.replicator.sockets = [self.socket]
            GlobalVar.player_state.replicator.sockets = [self.socket]
            self.socket.settimeout(TIMEOUT)
            self.ceck_timer = CeckTimer()  # si autostarta
        except sock.timeout:  # voglio che qualunque cosa succeda torni al menu e non crashi
            self.indietro()

    @staticmethod
    def gioca_carta(carta):
        fase = GlobalVar.game_state.fase_gioco.val
        # se devo ancora passare carte o se è il mio turno di giocare giocare
        if ((fase == Fase.PASSAGGIO_CARTE and len(GlobalVar.player_state.scambiate.val) < 3)
                or fase == Fase.GIOCO and GlobalVar.game_state.turno.val == GlobalVar.player_state.index.val):
            GlobalVar.player_state.param_scelta.val = carta  # basta questo per dire al server di aver giocato la carta
