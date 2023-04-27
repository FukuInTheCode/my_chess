from base_game import Game
import random
import math

class Bot(Game):
    
    def __init__(self, scr_w: int, scr_h: int, depth:int = 2) -> None:
        self.name = 'Bot Game'
        self.score = 0
        self.depth = depth
        super().__init__(scr_w, scr_h)
    def init(self):
        super().init()
    
    def leftclick(self, mx: int, my: int) -> None:
        mx = mx//self.board.sq_w + 1
        my = my//self.board.sq_h + 1
        
        tmp = self.clicked
        
        self.clicked = self.board.get_xy(mx, my)
        
        if self.clicked is not None and self.clicked.team != self.is_turn:
            self.clicked = None

        if tmp is not None and (mx, my) in tmp.get_faisable_position(self.board) and not self.board.in_check(*tmp.get_xy(), mx, my, tmp.team):
            self.is_turn *= -1
            self.board.move(*tmp.get_xy(), mx, my)
            self.clicked = None
            self.board.update()
            if self.board.in_checkmate(self.is_turn):
                self.checkmate(self.is_turn*-1)