# serve per passare i valori tra server e clients, così come mandare richieste a client

# formato: 'event:nome1=val1,nome2=val2,nome3=val3,\n'
#           game
#           player
#           ping

import socket as sock

# PARAMETRI
CODIFICA = 'utf-8'
BUFFER_SIZE = 2048

# TIPI
# server to client
EVENT_TYPE = 'EVENT'
GAME_TYPE = 'GAME'  # indirizzati al game state
PLAYER_PUBLIC_TYPE = 'PLAYER_PUBLIC'  # indirizzati al private player dentro al game state
PLAYER_LOCAL_TYPE = 'PLAYER_LOCAL'  # indirizzati al player state

# client to server
USERNAME_TYPE = 'USERNAME'
CARTA_TYPE = 'CARTA'
PING_TYPE = 'PING'


class Campo:  # serve semplicemente a tenere insieme nome e valore
    def __init__(self, nome, valore):
        self.nome = nome
        self.valore = valore


class Messaggio:
    codaMessaggi = []

    def __init__(self):
        self.tipo = None  # è una stringa
        self._campi = []
        self._stringa = None  # formattazione del messaggio in una stringa

    def add_campo(self, nome, valore):
        self._campi.append(Campo(nome, valore))

    def add_campo_int(self, nome, valore):
        self.add_campo(nome, str(valore))

    def get_campo(self, nome):
        for campo in self._campi:
            if campo.nome == nome:
                return campo.valore
        return None

    def get_campo_int(self, nome):
        num = self.get_campo(nome)
        if num is not None:
            return int(num)
        return None

    def _scrivi_stringa(self):
        stringa = self.tipo + ':'
        for campo in self._campi:
            stringa += campo.nome + '=' + campo.valore + ','
        stringa += '\n'
        self._stringa = stringa

    def _leggi_stringa(self):
        stringa = self._stringa.replace('\n', '')  # int teoria non serve ma non si sa mai
        stringa = stringa.split(':')
        self.tipo = stringa[0]
        campi = stringa[1].split(',')
        for c_str in campi:
            if c_str != '':  # l'ultima potrebbe essere vuota
                campo = c_str.split('=')
                self._campi.append(Campo(campo[0], campo[1]))

    def safe_send(self, socket):
        self._scrivi_stringa()
        try:
            socket.send(self._stringa.encode(CODIFICA))
            print(self._stringa)
        except ConnectionAbortedError:  # occore quando provo a mandare a uno che ha chiuso
            pass

    def set_stringa(self, stringa):
        self._stringa = stringa
        self._leggi_stringa()


def recv_messaggi(socket):
    try:
        stringa = socket.recv(BUFFER_SIZE).decode(CODIFICA)
        #  print('tcp:', stringa)
        str_messaggi = stringa.split('\n')  # serve se arrivano più messaggi alla volta
        for str_m in str_messaggi:
            if str_m != '':  # l'ultima potrebbe essere vuota
                messggio = Messaggio()
                messggio.set_stringa(str_m)  # crea messaggio dalla stringa
                Messaggio.codaMessaggi.append(messggio)  # aggiunge alla coda letta dal pl. cotroller e da game mode
    except sock.timeout:
        pass
    except ConnectionAbortedError:
        pass
    except ConnectionResetError:
        pass
