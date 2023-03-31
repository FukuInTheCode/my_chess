import pygame as pyg
from base_game import Game
from CONSTANT import BLACK

class Engine:
    def __init__(self, scr: pyg.Surface) -> None:
        """
        
        """
        self.game_type = Game(*scr.get_size())
        self.screen = scr
        self.is_running = True
        
        self.right_mouse = pyg.mouse.get_pos()
        
        pyg.display.set_caption(self.game_type.name)
        
        self.run()
        
    def draw(self) -> None:
        self.game_type.draw(self.screen)
        
    def run(self):
        while self.is_running:
            self.screen.fill(BLACK)
            self.draw()
            for event in pyg.event.get():
                if event.type == pyg.QUIT:
                    self.is_running = False
                    pyg.quit()
                    quit()
                    
                if event.type == pyg.MOUSEBUTTONDOWN and pyg.mouse.get_pressed()[0]:
                    
                    self.game_type.rightclick(*pyg.mouse.get_pos())
                    
                    
            pyg.display.flip()