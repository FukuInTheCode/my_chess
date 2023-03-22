import pygame as pyg
import math
from game import Game
import sys

class Engine():
    
    BLACK = (0, 0, 0)
    
    def __init__(self, screen: pyg.Surface) -> None:
        
        self.screen = screen
        
        self.game = Game(self)
        
        self.is_running = True
        
        self.run()
        
    def run(self) -> None:
        self.clock = pyg.time.Clock()
        


        
        while self.is_running:
            self.clock.tick(60)
            
            self.screen.fill(self.BLACK)
            
            self.game.update()
            self.game.draw()
            
            pyg.display.flip()
            
            for event in pyg.event.get():
                if event.type == pyg.QUIT:
                    self.is_running = False
                    pyg.quit()
                    sys.exit()   