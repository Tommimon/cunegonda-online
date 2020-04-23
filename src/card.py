# questa classe rappresenta una carta, sia lato server che client quindi non contiene grafica ma solo le var che la
# identifichano


class Card:
    # semi
    NESSUN_SEME = 0
    CUORI = 1
    QUADRI = 2
    FIORI = 3
    PICCHE = 4
    SEMI = [CUORI, QUADRI, FIORI, PICCHE]

    # valori ordinati dal meno potente al più potente
    NESSUN_VALORE = 0
    DUE = 2
    TRE = 3
    QUATTRO = 4
    CINQUE = 5
    SEI = 6
    SETTE = 7
    OTTO = 8
    NOVE = 9
    DIECI = 10
    JACK = 11
    DONNA = 12
    RE = 13
    ASSO = 14
    VALORI = [DUE, TRE, QUATTRO, CINQUE, SEI, SETTE, OTTO, NOVE, DIECI, JACK, DONNA, RE, ASSO]

    def __init__(self, valore=NESSUN_VALORE, seme=NESSUN_SEME):
        self.valore = valore
        self.seme = seme

    @staticmethod
    def del_carta(lista, cercata):
        for c in lista:
            if c.seme == cercata.seme and c.valore == cercata.valore:  # se ha stessi valori
                lista.remove(c)  # lo tolgo

    @staticmethod
    def contiene_carta(mano, cercata):  # in queste funzioni mano è semplicemente una lista di carte
        for c in mano:
            if c.seme == cercata.seme and c.valore == cercata.valore:
                return True
        return False

    @staticmethod
    def contiene_seme(mano, seme):
        for c in mano:
            if c.seme == seme:
                return True
        return False

    @staticmethod
    def carta_permessa(mano, seme, carta):
        if seme is None:  # se seme non c'è viene interpretato come se è il primo a giocare quindi sempre True
            return True
        if seme == carta.seme or not Card.contiene_seme(mano, seme):  # se seme giusto o se non ha quel seme
            return True
        return False

    @staticmethod
    def sort_carte(lista):
        ordinata = []
        ordine_semi = [Card.CUORI, Card.FIORI, Card.QUADRI, Card.PICCHE]  # cambio ordine per estetica
        for s in ordine_semi:
            for v in Card.VALORI:
                carta = Card(v, s)
                if Card.contiene_carta(lista, carta):
                    ordinata.append(carta)
        return ordinata



