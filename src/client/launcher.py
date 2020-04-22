from client.game_instance import GameInstance

print('launching game...')
newGame = GameInstance()  # creo la game instance
newGame.next_schermata = 'menu'  # mette come prossima schermata il menu
newGame.gestisci_schermate()  # apre la prossime schemata (che è il menu)
