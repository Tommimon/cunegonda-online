from server.game_mode import GameMode
from settings_reader import SettingsReader
from replicated.game_state import GameState
from server.global_var import GlobalVar
import socket as sock

# PARAMETRI
TIMEOUT = 0.02
SETTINGS_FILE = 'server_settings.txt'


while True:
    # try:
    settings = SettingsReader(SETTINGS_FILE)
    serverAddress = (settings.get_val('server_ip'), int(settings.get_val('server_port')))
    print(serverAddress)

    serverSocket = sock.socket(sock.AF_INET, sock.SOCK_STREAM)
    serverSocket.bind(serverAddress)
    serverSocket.settimeout(TIMEOUT)
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
