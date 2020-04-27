# si occupa della gestione delle regole e dei dati privati del server

from server.global_var import GlobalVar
from replicated.game_state import Fase
from server.player_private import PlayerPrivate
from server.deck import Deck, Card
from threading import Timer
from tcp_basics import safe_recv_var
from socket import timeout

# PARAMETRI
TIMEOUT = 0.02


class GameMode:
    def __init__(self):
        GlobalVar.game_mode = self
        self.game_state = GlobalVar.game_state
        self.lista_player = []
        self.replicators = [self.game_state.replicator]  # metto il replicator del game state
        for p in self.game_state.lista_player:
            self.replicators.append(p.replicator)  # aggiungo tutti i replicator dei public player
        self.mazzo = Deck()
        self.server_socket = None
        self.running = True
        self.pausa = False
        self.primo_in_prima = 0  # giocatore primo in prima mano (gira ogni partita)
        self.primo = 0
        self.ultimo = 3
        self.seme_giro = None
        self.questo_giro = []
        self.tutti_connessi = False  # vero sse ci sono 4 giocatori connessi
        self.g_disconnessi = []

    def attesa(self):
        while len(self.lista_player) < 4:
            try:
                new_socket, new_address = self.server_socket.accept()
                new_socket.settimeout(TIMEOUT)
                self.game_state.replicator.sockets.append(new_socket)  # ha effetto solo lato server
                new_private = PlayerPrivate(new_socket, len(self.lista_player))
                self.lista_player.append(new_private)
                self.replicators.append(new_private.player_state.replicator)  # replicator del nuovo player state
                print('conncted', new_address)
            except timeout:
                pass
            safe_recv_var(self.replicators)  # comincio già a ricevere per i ceck
        self.tutti_connessi = True
        for g in self.game_state.lista_player:  # caccio una refreshata agli username
            g.username.rep_val()
        self.dai_carte()
        self.game_loop()

    def accetta_riconnessione(self):
        if len(self.g_disconnessi) > 0:
            try:
                new_socket, address = self.server_socket.accept()
                new_socket.settimeout(TIMEOUT)
                self.game_state.replicator.sockets.append(new_socket)  # avevo rimosso il vecchio socket del disconnesso
                private = self.g_disconnessi.pop()
                private.socket = new_socket  # questo serve per poterlo ritogliere
                private.player_state.replicator.sockets = [new_socket]  # avevo svuotato ore metto il nuovo
                self.game_state.replicator.refresh_all()  # refresh game_state a tutti, (basterebbe questo nuovo player)
                for p in self.game_state.lista_player:  # refresh tutti per tutti, non efficiente ma tanto viene
                    p.replicator.refresh_all()          # eseguito solo se uno esce e rientra
                private.player_state.replicator.refresh_all()  # refresho sono per il player giusto
                if len(self.g_disconnessi) == 0:
                    self.tutti_connessi = True
            except timeout:
                pass

    def disconnetti(self, private):
        sock = private.socket
        self.game_state.replicator.sockets.remove(sock)  # tolgo il socket del disconnesso
        private.player_state.replicator.sockets = []  # ce ne è uno solo quindi posso fare così
        self.g_disconnessi.append(private)
        self.game_state.lista_player[private.player_state.index.val].username.val = '---'  # così gli altri lo vedono
        self.tutti_connessi = False

    def dai_carte(self):
        self.mazzo.carte = []
        self.mazzo.crea_carte()
        self.mazzo.mischia()
        for giocatore in self.lista_player:
            carte = self.mazzo.pesca_n(13)
            for c in carte:
                giocatore.player_state.mano.val.append(c)
            giocatore.player_state.mano.rep_val()

    def game_loop(self):
        self.game_state.fase_gioco.val = Fase.PASSAGGIO_CARTE
        while self.running:
            safe_recv_var(self.replicators)
            self.accetta_riconnessione()

    def carta_client(self, index_g, carta):  # controlla in che fase siamo e se si può adoperare la carta e poi faù
        giocatore = self.lista_player[index_g]  # giocatore è un private player type
        if Card.contiene_carta(giocatore.player_state.mano.val, carta):  # se possiede davvero questa carta
            if self.game_state.fase_gioco.val == Fase.PASSAGGIO_CARTE:  # se le stiamo passando la metto nelle scambiate
                if len(giocatore.player_state.scambiate.val) < 3:  # se non ne ho già scambiate 3
                    self.metti_in_passate(giocatore, carta)
            elif self.game_state.fase_gioco.val == Fase.GIOCO and (not self.pausa):  # se stiamo giocando e non è pausa
                if index_g == self.game_state.turno.val:  # se è il suo turno
                    if (index_g == self.primo or Card.carta_permessa(giocatore.player_state.mano.val,
                                                                     self.game_state.seme_primo.val, carta)):
                        self.metti_in_giocata(index_g, carta)

    def metti_in_giocata(self, index, carta):
        Card.del_carta(self.lista_player[index].player_state.mano.val, carta)  # tolgo la carta dalla mano
        self.lista_player[index].player_state.mano.rep_val()  # non lo fa in automatico credo
        self.game_state.lista_player[index].carta_giocata.val = carta  # la metto nelle giocate
        self.questo_giro.append(carta)  # mi salvo le carte giocate nella gamemode
        if self.game_state.turno.val == self.primo:
            self.game_state.seme_primo.val = carta.seme  # il primo decide il seme del giro
        if self.game_state.turno.val == self.ultimo:
            self.risolvi_questo_giro()
        else:
            turno = (self.game_state.turno.val + 1) % 4
            self.game_state.turno.val = turno

    def metti_in_passate(self, giocatore, carta):
        Card.del_carta(giocatore.player_state.mano.val, carta)  # tolgo la carta dalla mano
        giocatore.player_state.mano.rep_val()  # non lo fa in automatico credo
        giocatore.player_state.scambiate.val.append(carta)  # la metto in quelle scambiate
        giocatore.player_state.scambiate.rep_val()
        self.ceck_fine_passaggio()

    def ceck_fine_passaggio(self):
        for gioc in self.lista_player:
            state = gioc.player_state
            if len(state.scambiate.val) < 3:
                return
        self.passa_carte()  # si occupa anche di fare self.game_state.fase_gioco.val = GIOCO

    def passa_carte(self):
        for gioc in self.lista_player:
            state = gioc.player_state
            index = (self.lista_player.index(gioc) - 1) % 4  # prendo il giocatore precedente
            for carta in state.scambiate.val:
                self.lista_player[index].player_state.mano.val.append(carta)  # gli passo la carta
            self.lista_player[index].player_state.mano.rep_val()
            self.game_state.fase_gioco.val = Fase.GIOCO
            state.scambiate.val = []  # tolgo tutte le scambiate

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
            if carta.seme == self.game_state.seme_primo.val:  # se è seme che comanda
                if carta.valore > val_max:  # se è più grande del max
                    val_max = carta.valore
                    index_max = self.questo_giro.index(carta)
        # adesso index_max è il primo ma contato a partire dal primo attuale quindi è di quanto devo spostarmi
        vincitore = (self.primo + index_max) % 4
        return vincitore

    def risolvi_questo_giro(self):
        punteggio = self.calcola_punteggio()
        vincitore = self.trova_vincitore()
        print('points: ' + str(punteggio) + ' to ' + str(vincitore))
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
            g.carta_giocata.val = Card()
        if len(self.lista_player[0].player_state.mano.val) == 0:  # se un giocatore non ha carte (tutti le hanno finite)
            self.check_cappotto()
            for i in range(len(self.lista_player)):  # aggiorno punteggi totali per tutti
                g_privat = self.lista_player[i]
                g_public = self.game_state.lista_player[i]
                g_public.punteggio_tot.val = g_public.punteggio_tot.val + g_privat.punteggio
                g_privat.punteggio = 0
                g_privat.carte_prese = []
            self.game_state.fase_gioco.val = Fase.FINE_PARTITA  # così gli HUD scrivono fine partita
            t = Timer(10, self.fine_partita)
            t.start()
        else:
            self.pausa = False
            self.game_state.turno.val = self.primo
            self.game_state.seme_primo.val = Card.NESSUN_SEME

    def fine_partita(self):
        self.game_state.cont_partita.val = self.game_state.cont_partita.val + 1
        self.pausa = False
        self.primo_in_prima = (self.primo_in_prima + 1) % 4
        self.primo = self.primo_in_prima
        self.ultimo = (self.primo - 1) % 4
        self.game_state.turno.val = self.primo
        self.game_state.seme_primo.val = Card.NESSUN_SEME
        self.dai_carte()
        self.game_state.fase_gioco.val = Fase.PASSAGGIO_CARTE
