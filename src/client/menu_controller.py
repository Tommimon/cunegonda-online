# gestisce gli eventi di pygame, in questo caso solo quit e mouse (che passa all'HUD)

from client.menu_GUI import MenuGUI
from client.global_var import GlobalVar
import pygame as pg

FPS = 60  # Frames per second.


class MenuController:
    def __init__(self):
        GlobalVar.player_controller = self
        self.GUI = MenuGUI()  # creo HUD e mi salvo una ref
        self.clock = pg.time.Clock()  # inizializzo clock
        self.running = True

    def loop(self):
        while self.running:
            self.clock.tick(FPS)  # mi fa andare al giusto frame rate
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    self.quit()
                if event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
                    self.GUI.mouse_click(event.pos)
            self.GUI.display()

    def quit(self):
        self.running = False
