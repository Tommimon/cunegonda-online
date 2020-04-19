# questa classe rappresenta un mazzo quindi contiene tante carte e i metodi per agire sul mazzo

from card import *
import random as rand


class Deck:
    def __init__(self):
        self.carte = []
        self.crea_carte()

    def crea_carte(self):
        for val in Card.VALORI:  # per ogni valore
            for seme in Card.SEMI:  # per ogni seme
                self.carte.append(Card(val, seme))  # creo una carta e la aggiungo alla lista

    def mischia(self):
        rand.shuffle(self.carte)

    def pesca_n(self, n):
        pescate = []
        for i in range(n):
            pescate.append(self.carte.pop(0))
        return pescate
