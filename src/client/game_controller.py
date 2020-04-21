# gestisce gli eventi di pygame per il gioco vero e proprio

from client.game_GUI import *
from comunication import *
from replicated.game_state import *
from tcp_basics import safe_recv_var

FPS = 60  # Frames per second.
TIMEOUT = 0.2


class GameController:
    def __init__(self):
        GlobalVar.player_controller = self
        self.GUI = GameGUI()  # creo HUD e mi salvo una ref
        self.socket = sock.socket(sock.AF_INET, sock.SOCK_STREAM)
        self.replicators = [GlobalVar.player_state.replicator, GlobalVar.game_state.replicator]  # mi salvo tutti i...
        for g in GlobalVar.game_state.lista_player:  # replicator, nel for quelli dei player_public
            self.replicators.append(g.replicator)
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
        self.quit()

    def connettiti(self):  # se non mi connetto al server torno al menu
        try:
            self.socket.connect(GlobalVar.game_instance.server_address)
            GlobalVar.game_state.replicator.sockets = [self.socket]
            GlobalVar.player_state.replicator.sockets = [self.socket]
            self.socket.settimeout(TIMEOUT)
            mess = Messaggio()
            mess.tipo = USERNAME_TYPE
            mess.add_campo('username', GlobalVar.game_instance.username)
            mess.safe_send(self.socket)
        except:
            self.indietro()

    def gioca_carta(self, carta):
        fase = GlobalVar.game_state.fase_gioco
        if ((fase == PASSAGGIO_CARTE and len(GlobalVar.player_state.scambiate) < 3)  # se devo ancora passare carte
                or fase == GIOCO and GlobalVar.game_state.turno == GlobalVar.player_state.index.val):  # o se devo giocare
            mess = Messaggio()
            mess.tipo = CARTA_TYPE
            mess.add_campo_int('seme', carta.seme)
            mess.add_campo_int('valore', carta.valore)
            mess.safe_send(self.socket)
            print(len(GlobalVar.player_state.mano))
