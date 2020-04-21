from server.game_mode import *
from settings_reader import *
from replicated.game_state import *

SETTINGS_FILE = 'server_settings.txt'


while True:
    # try:
    settings = SettingsReader(SETTINGS_FILE)
    serverAddress = (settings.get_val('server_ip'), int(settings.get_val('server_port')))
    print(serverAddress)

    serverSocket = sock.socket(sock.AF_INET, sock.SOCK_STREAM)
    serverSocket.bind(serverAddress)
    serverSocket.listen()
    print('server ready')

    GlobalVar.game_state = GameState(auth=True)

    gameMode = GameMode()
    gameMode.server_socket = serverSocket
    gameMode.attesa()

    serverSocket.close()
    print('closing server...')
    # except:
    # print('fatal error rebooting...')
