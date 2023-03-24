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
                 
            if pyg.mouse.get_pressed()[0]:
                cursor_x, cursor_y = pyg.mouse.get_pos()
                cursor_x //= self.game.square_size_w
                cursor_y //= self.game.square_size_h
                cursor_x = int(cursor_x)
                cursor_y = int(cursor_y)
                if self.game.clicked is not None and self.game.clicked.team == self.game.is_turn:
                    if (cursor_x, cursor_y) in self.game.clicked.get_moves(True):
                        self.game.clicked.set_pos(cursor_x, cursor_y)
                        if self.game.board[cursor_y][cursor_x] is not None:
                            self.game.pieces.remove(self.game.board[cursor_y][cursor_x])
                        self.game.is_turn = not self.game.is_turn
                
                self.game.clicked = self.game.board[cursor_y][cursor_x]
            pyg.display.flip()
            
            for event in pyg.event.get():
                if event.type == pyg.QUIT:
                    self.is_running = False
                    pyg.quit()
                    sys.exit()