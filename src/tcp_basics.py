from socket import socket, AF_INET, SOCK_STREAM, timeout
#  from varname import varname
from json import dumps, loads


def server_init(server_ip, server_port):  # fa la passive open e restituisce il socket del server
    server_address = (server_ip, server_port)
    server_socket = socket(AF_INET, SOCK_STREAM)
    server_socket.bind(server_address)
    server_socket.listen()
    return server_socket


def client_init(server_ip, server_port):  # fala active oopen e restituisce il socket del client
    server_address = (server_ip, server_port)
    client_socket = socket(AF_INET, SOCK_STREAM)
    client_socket.connect(server_address)
    return client_socket


# PARAMETRI
CODIFICA = 'utf-8'
BUFFER_SIZE = 2048


def safe_send(messaggio, sock):
    try:
        sock.send(messaggio.encode(CODIFICA))
        # print('tcp-out', messaggio)
    except ConnectionResetError:
        pass
    except ConnectionAbortedError:  # occore quando provo a mandare a uno che ha chiuso
        pass


def safe_recv_var(replicators):
    sockets = []
    for r in replicators:  # metto tutti i socket nella lista ma una sola volta
        for s in r.sockets:
            if not(s in sockets):
                sockets.append(s)
    for sock in sockets:
        try:
            stringa = sock.recv(BUFFER_SIZE).decode(CODIFICA)
            #  print('tcp-in ', stringa)
            messaggi = stringa.split('\n')  # serve se arrivano più messaggi alla volta
            messaggi.remove('')  # l'ultima potrebbe essere vuota
            for mess in messaggi:
                for r in replicators:
                    trovato = r.rec_var(mess)
                    if trovato:  # non serve continuare la ricerca
                        break
        except timeout:
            pass
        except ConnectionAbortedError:
            pass
        except ConnectionResetError:
            pass


class Replicator:  # contiene le info per replicare le variabili
    def __init__(self, rep_id, auth=False, sockets=[]):
        self.id = rep_id  # il nome che che mi dice dove stanno le variabili che replico
        self.auth = auth  # mi dice se ho autorità di modificare variabili usanodo questo replicator
        # rappresenta l'auth di default, può essere sovrascritta da quella della var stessa
        self.sockets = sockets  # socket a cui inviare
        self.vars = []  # variabili associate

    def manda_var(self, stringa):
        messaggio = self.id + ':' + stringa + '\n'
        for s in self.sockets:
            safe_send(messaggio, s)

    @staticmethod
    def split_id_string(messaggio):  # trova restituisce l'id che sta all'inizio della stringa
        index = messaggio.index(':')
        rep_id = messaggio[:index]
        stringa = messaggio[index+1:]
        return rep_id, stringa

    @staticmethod
    def can_match(string, pattern):  # guarda se il primo può combaciare con il secondo considerando gli * come jolly
        if len(string) != len(pattern):
            return False
        for i in range(len(pattern)):
            if pattern[i] != '*' and pattern[i] != string[i]:
                return False
        return True

    def rec_var(self, messaggio):  # restituisce True solo se questo è il suo replicator così posso smettere di cercare
        rep_id, stringa = Replicator.split_id_string(messaggio)
        if not Replicator.can_match(rep_id, self.id):
            return False  # false se questo non è il replicator per questo messaggio (se il nome non può andare bene)
        var_id, stringa_serial = Replicator.split_id_string(stringa)
        for v in self.vars:  # cerco la var giusta
            if v.get_id() == var_id:
                if not v.calcola_auth():  # se non ho auth accetto la modifica
                    v.custom_load(stringa_serial)
        return True  # anche se non modifico perché non ho auth oppure non esiste la var ma comunque questo era il
        # replicator giusto quindi restituisco True così capisce che non deve cercare in altri


class NoAuthority(Exception):  # Raisato quando provo a modificare una var su cui non ho auth
    pass


# questa class si occupa di tenere aggiornato il valore di val accross the network per i tipo base, per le classi
# scritte dall'utente si limita ad aggiornarne gli attributi ma l'oggetto deve essere già esistente per tutti i connessi
# non funziona con liste di oggetti o oggetti di oggetti, gli oggetti dell'utente possono solo essere assegnati
# direttamente a val
# nota che con on_rep posso creare delle funzioni a distanza passando i parametri come valore di questa variabile e
# mettende la funzione che deve essere chiamata in on_rep
class ReplicatedVar:  # ogni volta che modifico questa var usa il Replicator per aggiornarla su gli altri
    def __init__(self, val, replicator, id_name=None, auth=None, on_rep=None):
        self.creating = True
        if id_name is None:
            #  self._id = varname()  # pare non funzioni se ReplicatedVar è assegnata a un attributo
            pass
        else:
            self._id = id_name
        self.val = val  # aggiunge attributo val
        self.replicator = replicator
        self.auth = auth
        self.on_rep = on_rep  # cosa fare se arriva il messaggio di cambio di valore
        self.replicator.vars.append(self)  # si aggiunge alle var del replicator
        self.creating = False

    def get_id(self):
        return self._id

    def set_no_rep(self, val):  # usare dall'esterno per settare il valore di val SENZA replicare
        # val è usato come stringa in questa classe, se si cambia vanno cambiate le stringhe
        # usato qui e in __setattr__
        super(ReplicatedVar, self).__setattr__('val', val)

    @staticmethod
    def _json_default(obj):
        lis = obj.__dict__
        lis['__obj__'] = True  # aggiungo il fatto che non sia una normale dict ma un oggetto
        print('lis', lis)
        return lis

    def _serial(self):
        return dumps(self.val, default=ReplicatedVar._json_default)

    def _load_obj(self, dictionary):
        del dictionary['__obj__']
        for key in dictionary:  # assegna i valori
            setattr(self.val, key, dictionary[key])  # non setta val ma gli attributi di val nome per nome

    def custom_load(self, stringa):
        data = loads(stringa)
        # possibili tipi di dato: None, bool, int, float, str, list, dict
        if type(data) == dict and '__obj__' in data:
            self._load_obj(data)
        else:
            self.set_no_rep(data)
        if self.on_rep is not None:
            self.on_rep()  # attiva azione da fare quando viene modificato il valore da chi ha auth

    def calcola_auth(self):  # si occupa di gestire le contraddizioni tra auth della var e del replicator
        if self.auth is None:
            return self.replicator.auth  # se quella della var è none allore usiamo quella del replicator
        return self.auth  # se no quella della var è dominante

    def rep_val(self):  # usare da fuori per aggiornare e dire a tutti senza cambiare
        if self.calcola_auth():
            stringa = self._id + ':' + self._serial()  # aggiungo id della var
            self.replicator.manda_var(stringa)
        else:
            raise NoAuthority

    def __setattr__(self, key, value):
        super(ReplicatedVar, self).__setattr__(key, value)
        if not self.creating and key == 'val':  # in init skippo questa parte
            self.rep_val()
