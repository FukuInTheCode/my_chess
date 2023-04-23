import pygame as pyg
from base_game import Game
from openings_puzzle import OpeningPuzzle
from bot import Bot
from CONSTANT import BLACK

class Engine:
    def __init__(self, scr: pyg.Surface) -> None:
        tmp = scr.get_size()
        self.game_type = Game(tmp[0]*0.90, tmp[1]*0.90)
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
                    
                    mou_x, mou_y = pyg.mouse.get_pos()
                    
                    if (0 <= mou_x <= self.game_type.w) and (0<= mou_y <= self.game_type.h):
                        self.game_type.leftclick(mou_x, mou_y)
                        
                    else:
                        self.game_type.subgame(mou_x, mou_y)
                        
                elif event.type == pyg.KEYDOWN and event.key == pyg.K_r:
                    self.game_type.rotate()
                    
                elif event.type == pyg.KEYDOWN and event.key == pyg.K_LEFT:
                    self.game_type.K_left()
                    
                elif event.type == pyg.KEYDOWN and event.key == pyg.K_RIGHT:
                    self.game_type.K_right()
 
                    
            pyg.display.flip()