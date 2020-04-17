#  questa classe si occupa di leggere e scrivere dei valori da un file specificato


class SettingsReader:
    def __init__(self, file):
        self.file = file
        self.lista_settings = []  # ogni setting è una lista di nome e valore (in stringa)
        self._leggi_file()

    def _leggi_file(self):
        file = open(self.file, 'r')
        for riga in file:
            riga = riga.split(' =')  # adesso riga è una lista che comprende nome del campo e valore del campo
            val = riga[1].replace('\n', '')  # devo togliere il carattere di a capo
            val = val.replace(' ', '')  # togliere gli spazi è importante anche per togliere quello iniziale se c'è
            self.lista_settings.append([riga[0], val])  # metto nome e valore nella lista
        print('imported settings:', self.lista_settings)

    def get_val(self, nome):  # restituisco sempre una stringa, tornare al tipo giiusto sono problemi di chi chiama
        for setting in self.lista_settings:
            if setting[0] == nome:  # se è il nome giusto
                if setting[1] == '':  # se è vuoto allora faccio inserire
                    return input(nome + ': ')
                else:
                    return setting[1]  # se  no restituisco
