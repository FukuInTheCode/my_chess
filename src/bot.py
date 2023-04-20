from base_game import Game
from threading import *
import random
import math

class Bot(Game):
    
    def __init__(self, scr_w: int, scr_h: int, depth:int = 2) -> None:
        self.name = 'Bot Game'
        self.score = 0
        self.depth = depth
        self.eval_thread = Thread(target=self.evalutate, daemon=True)
        super().__init__(scr_w, scr_h)
        
        
    def init(self):
        super().init()
        self.eval_thread.start()
        
    def evalutate(self):
        self.score = 0
        tmp = 0
        for piece in self.board.pieces:
            
            if piece.team != self.is_turn:
                continue
            
            for mv in piece.get_faisable_position(self.board):
                bd = self.board.copy()
                bd.move(*piece.get_xy(), *mv)
                bd.update()
                bd.print()
                self.score += self.recursion_eval(1, bd, self.is_turn)/(2*self.depth)
                tmp += 1
                
        self.score /= tmp
        print(self.score)

                
    def recursion_eval(self, n:int, board, team:int):
        
        tmp = self.count_pts(board)
        
        if n >= 2*self.depth:
            return tmp
        
        for p in board.pieces:
            
            mvs = p.get_faisable_position(board)
            if p.team != team or len(mvs) == 0:
                continue
            for mv in random.choices(k=math.ceil(len(mvs)/2), population=mvs):
                bd = board.copy()
                bd.move(*p.get_xy(), *mv)
                bd.update()
                tmp += self.recursion_eval(n+1, bd, team*-1)
        return tmp
            
            
    def run_eval(self):
        self.eval_thread.start()
        
    def count_pts(self, board):
        ret = 0
        for piece in board.pieces:
            ret += piece.point
            
        return ret
    
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
            self.run_eval()
            if self.board.in_checkmate(self.is_turn):
                self.checkmate(self.is_turn*-1)