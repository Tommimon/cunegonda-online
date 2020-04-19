# si occupa della gestione delle regole e dei dati privati del server

from server.global_var import *
from replicated.game_state import *
from server.player_private import *
from server.deck import *
from threading import Timer

# PARAMETRI
TIMEOUT = 0.2


class GameMode:
    def __init__(self):
        GlobalVar.game_mode = self
        self.game_state = GlobalVar.game_state
        self.lista_player = []
        self.mazzo = Deck()
        self.server_socket = None
        self.running = True
        self.pausa = False
        self.primo_in_prima = 0  # giocatore primo in prima mano (gira ogni partita)
        self.primo = 0
        self.ultimo = 3
        self.seme_giro = None
        self.questo_giro = []

    def attesa(self):
        while len(self.lista_player) < 4:
            socket, address = self.server_socket.accept()
            socket.settimeout(TIMEOUT)
            self.game_state.lista_socket.append(socket)  # ha effetto solo lato server
            new_private = PlayerPrivate(socket)
            new_private.player_state.set_rep_index(len(self.lista_player))  # la prima volta è 0
            self.lista_player.append(new_private)
            print('conncted', address)
        self.dai_carte()
        self.game_loop()

    def dai_carte(self):
        self.mazzo.carte = []
        self.mazzo.crea_carte()
        self.mazzo.mischia()
        for giocatore in self.lista_player:
            carte = self.mazzo.pesca_n(13)
            for c in carte:
                giocatore.player_state.add_to_mano(c)

    def game_loop(self):
        self.game_state.set_rep_fase(PASSAGGIO_CARTE)
        while self.running:
            for giocatore in self.lista_player:
                recv_messaggi(giocatore.socket)
                for mess in Messaggio.codaMessaggi:
                    self.client_message(giocatore, mess)
                Messaggio.codaMessaggi = []  # svuoto perché ho usato

    def client_message(self, giocatore, messaggio):
        if messaggio.tipo == USERNAME_TYPE:
            print('set username', messaggio.get_campo('username'))
            index = self.lista_player.index(giocatore)
            # metto nel player pubblico l'username che ho letto dal messaggio del client
            self.game_state.lista_player[index].set_rep_username(messaggio.get_campo('username'))
        elif messaggio.tipo == CARTA_TYPE:
            carta = Card(messaggio.get_campo_int('valore'), messaggio.get_campo_int('seme'))
            print('giocata', carta.seme, carta.valore)
            self.carta_client(giocatore, carta)

    @staticmethod
    def possiede_carta(giocatore, cercata):
        for c in giocatore.player_state.mano:
            if c.seme == cercata.seme and c.valore == cercata.valore:
                return True
        return False

    @staticmethod
    def possiede_seme(giocatore, seme):
        for c in giocatore.player_state.mano:
            if c.seme == seme:
                return True
        return False

    def carta_client(self, giocatore, carta):  # controlla in che fase siamo e se si può adoperare la carta e poi fa
        if GameMode.possiede_carta(giocatore, carta):  # se possiede davvero questa carta
            if self.game_state.fase_gioco == PASSAGGIO_CARTE:  # se le stiamo passando la metto nelle scambiate
                if len(giocatore.player_state.scambiate) < 3:  # se non ne ho già scambiate 3
                    self.metti_in_passate(giocatore, carta)
            elif self.game_state.fase_gioco == GIOCO and (not self.pausa):  # se stiamo giocando e non è pausa
                index = self.lista_player.index(giocatore)
                if index == self.game_state.turno:  # se è il suo turno
                    if (index == self.primo or (not GameMode.possiede_seme(giocatore, self.seme_giro))
                            or self.seme_giro == carta.seme):  # se è primo o non ha questo seme o è seme giusto
                        self.metti_in_giocata(index, carta)

    def metti_in_giocata(self, index, carta):
        self.lista_player[index].player_state.del_rep_from_mano(carta)  # tolgo la carta dalla mano
        self.game_state.lista_player[index].set_rep_carta_gioc(carta)  # la metto nelle giocate
        self.questo_giro.append(carta)  # mi salvo le carte giocate nella gamemode
        if self.game_state.turno == self.primo:
            self.seme_giro = carta.seme  # il primo decide il seme del giro
        if self.game_state.turno == self.ultimo:
            self.risolvi_questo_giro()
        else:
            turno = (self.game_state.turno + 1) % 4
            self.game_state.set_rep_turno(turno)

    def metti_in_passate(self, giocatore, carta):
        giocatore.player_state.del_rep_from_mano(carta)  # tolgo la carta dalla mano
        giocatore.player_state.add_to_scambiate(carta)  # la metto in quelle scambiate
        self.ceck_fine_passaggio()

    def ceck_fine_passaggio(self):
        for gioc in self.lista_player:
            state = gioc.player_state
            if len(state.scambiate) < 3:
                return
        self.passa_carte()  # si occupa anche di fare self.game_state.set_rep_fase(GIOCO)

    def passa_carte(self):
        for gioc in self.lista_player:
            state = gioc.player_state
            for carta in state.scambiate:
                index = (self.lista_player.index(gioc) - 1) % 4  # prendo il giocatore precedente
                self.lista_player[index].player_state.add_to_mano(carta)  # gli passo la carta
            self.game_state.set_rep_fase(GIOCO)
            state.clear_scambiate()  # tolgo tutte le scambiate

    def calcola_punteggio(self):
        punteggio = 10  # valore di base
        for carta in self.questo_giro:  # contro punti negativi
            if carta.seme == Card.CUORI:
                punteggio -= carta.valore  # il valore della carta solo già i punti neg per i cuori
            elif carta.seme == Card.PICCHE and carta.valore == Card.DONNA:  # se è cuneconda
                punteggio -= 26
        return punteggio

    def trova_vincitore(self):
        val_max = self.questo_giro[0].valore  # trovo carta vincente
        index_max = 0
        for carta in self.questo_giro:
            if carta.seme == self.seme_giro:  # se è seme che comanda
                if carta.valore > val_max:  # se è più grande del max
                    val_max = carta.valore
                    index_max = self.questo_giro.index(carta)
        # adesso index_max è il primo ma contato a partire dal primo attuale quindi è di quanto devo spostarmi
        vincitore = (self.primo + index_max) % 4
        return vincitore

    def risolvi_questo_giro(self):
        punteggio = self.calcola_punteggio()
        vincitore = self.trova_vincitore()
        print('punteggio: ' + str(punteggio) + ' a ' + str(vincitore))
        self.primo = vincitore
        self.ultimo = (self.primo - 1) % 4
        self.pausa = True
        self.lista_player[vincitore].punteggio += punteggio  # assegno i punti
        self.lista_player[vincitore].carte_prese += self.questo_giro  # metto tutte le carte giocate nelle prese di vinc
        self.questo_giro = []  # svuoto copia locale
        t = Timer(5, self.fine_turno)  # lascio vedere le carte per 5 sec
        t.start()

    @staticmethod
    def ha_preso_carta(giocatore, carta):
        for c in giocatore.carte_prese:
            if c.seme == carta.seme and c.valore == carta.valore:
                return True
        return False

    def check_cappotto(self):
        for g_esaminato in self.lista_player:
            if GameMode.ha_preso_carta(g_esaminato, Card(Card.DONNA, Card.PICCHE)):  # se ha cunegonda
                for val in Card.VALORI:
                    if not GameMode.ha_preso_carta(g_esaminato, Card(val, Card.CUORI)):  # manca un cuore
                        return  # se quello che ha la cune non ha un cuore allora niente cappotto
                # se arrivo qui allor aho cappotto quindi setto tutti a -20 tranne g a cui do 60
                for g_da_cambiare in self.lista_player:
                    if g_da_cambiare == g_esaminato:
                        g_da_cambiare.punteggio = 60
                    else:
                        g_da_cambiare.punteggio = -20

    def fine_turno(self):
        for g in self.game_state.lista_player:  # svuoto giocate in ogni caso
            g.set_rep_carta_gioc(Card())
        if len(self.lista_player[0].player_state.mano) == 0:  # se un giocatore non ha carte (tutti le hanno finite)
            self.check_cappotto()
            for i in range(len(self.lista_player)):  # aggiorno punteggi totali per tutti
                g_privat = self.lista_player[i]
                g_public = self.game_state.lista_player[i]
                g_public.set_rep_punteggio_tot(g_public.punteggio_tot + g_privat.punteggio)
                g_privat.punteggio = 0
                g_privat.carte_prese = []
            self.game_state.set_rep_fase(FINE_PARTITA)  # così gli HUD scrivono fine partita
            t = Timer(10, self.fine_partita)
            t.start()
        else:
            self.pausa = False
            self.game_state.set_rep_turno(self.primo)

    def fine_partita(self):
        self.game_state.set_rep_cont_partita(self.game_state.cont_partita + 1)
        self.pausa = False
        self.primo_in_prima = (self.primo_in_prima + 1) % 4
        self.primo = self.primo_in_prima
        self.ultimo = (self.primo - 1) % 4
        self.game_state.set_rep_turno(self.primo)
        self.dai_carte()
        self.game_state.set_rep_fase(PASSAGGIO_CARTE)
