# manda perpetuamente un segnale ogni CECK_DELAY secondi al server per dimostrare di essere connesso
from threading import Timer
from client.global_var import GlobalVar

CECK_DELAY = 2


class CeckTimer:
    def __init__(self):
        self.timer = Timer(CECK_DELAY, self.reset)
        self.timer.start()
        self.running = True

    def reset(self):
        if self.running:
            self.manda_ceck()
            self.timer = Timer(CECK_DELAY, self.reset)
            self.timer.start()

    def stop(self):
        self.timer.cancel()
        self.running = False

    @staticmethod
    def manda_ceck():
        GlobalVar.player_state.param_ceck.val = 0  # 0 significa senza errori ma l'importante è settarlo così comunica
        # print('ceck mandato')
