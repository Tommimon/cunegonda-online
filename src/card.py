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

    def __init__(self, seme, valore):
        self.seme = seme
        self.valore = valore
