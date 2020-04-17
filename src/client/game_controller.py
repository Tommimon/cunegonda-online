# gestisce gli eventi di pygame per il gioco vero e proprio

from client.game_HUD import *
from comunication import *
from replicated.game_state import *

FPS = 60  # Frames per second.
TIMEOUT = 0.2


class GameController:
    def __init__(self):
        GlobalVar.player_controller = self
        self.HUD = GameHUD()  # creo HUD e mi salvo una ref
        self.socket = sock.socket(sock.AF_INET, sock.SOCK_STREAM)
        self.connettiti()
        self.clock = pg.time.Clock()  # inizializzo clock
        self.running = True

    def loop(self):
        while self.running:
            self.clock.tick(FPS)  # mi fa andare al giusto frame rate
            self.server_events()
            self.pygame_events()
            self.HUD.display()

    def pygame_events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.quit()
            if event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
                self.HUD.mouse_click(event.pos)

    def server_events(self):
        recv_messaggi(self.socket)  # riempie la lista
        for messaggio in Messaggio.codaMessaggi:
            if messaggio.tipo == GAME_TYPE:
                GlobalVar.game_state.risolvi_messaggio(messaggio)
            if messaggio.tipo == PLAYER_PUBLIC_TYPE:
                GlobalVar.game_state.lista_player[messaggio.get_campo_int('index')].risolvi_messaggio(messaggio)
            if messaggio.tipo == PLAYER_LOCAL_TYPE:
                GlobalVar.player_state.risolvi_messaggio(messaggio)
        Messaggio.codaMessaggi = []  # li ho fatti quindi vanno tolti

    def quit(self):
        self.running = False

    def indietro(self):
        GlobalVar.game_instance.next_schermata = 'menu'
        self.quit()

    def connettiti(self):  # se non mi connetto al server torno al menu
        try:
            self.socket.connect(GlobalVar.game_instance.server_address)
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
                or fase == GIOCO and GlobalVar.game_state.turno == GlobalVar.player_state.index):  # o se devo giocare
            mess = Messaggio()
            mess.tipo = CARTA_TYPE
            mess.add_campo_int('seme', carta.seme)
            mess.add_campo_int('valore', carta.valore)
            mess.safe_send(self.socket)
            print(len(GlobalVar.player_state.mano))
