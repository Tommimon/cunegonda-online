# qui dichiaro le var statiche che voglio siano accessibili ovunque


class GlobalVar:
    game_instance = None
    screen = None  # lo schermo creato nella game instance che persiste sempre
    player_controller = None
    player_HUD = None
    game_state = None
    player_state = None
