import pygame as pyg
from CONSTANT import BLACK_SQUARE_COLOR, WHITE_SQUARE_COLOR

class Board:
    def __init__(self, w:int, h:int, scr_w:int, scr_h:int) -> None:
        self.board = [[None for i in range(w)] for j in range(h)]
        self.w = w
        self.h = h
        self.sq_w = int(scr_w//w)
        self.sq_h = int(scr_h//h)
        
        self.last_moved = None
        
        self.pieces = []
        
    def get_xy(self, x:int, y:int):
        return self.board[y-1][x-1]
    
    def is_xy_none(self, x:int, y:int)->bool:
        return self.get_xy(x, y) == None
    
    def set_to(self, piece):
        if self.is_xy_none(*piece.get_xy()):
            self.board[piece.y - 1][piece.x - 1] = piece
            
        else:
            raise Exception('Try to set two pieces on the same square or position out of the board boundaries')
        
    def add(self, piece) -> None:
        self.pieces.append(piece)
        
    def move(self, x, y, tox, toy) -> None:
        
        for piece in self.pieces:
            piece.last_move = None
        
        tmp = self.get_xy(tox, toy)
        
        self.last_moved = self.get_xy(x, y)
        
        self.last_moved.set_pos(tox, toy)
        
        if tmp is not None:
            self.pieces.remove(tmp)
            
        elif self.last_moved.type == 'P':
            if tox - x != 0:
                self.pieces.remove(self.get_xy(tox, y))

    def check_xy(self, x, y)->bool:
        if (0<x<=self.w) and (0<y<=self.h):
            return True
        
        return False
    
    def draw(self, scr:pyg.Surface) -> None:
        
        for i in range(self.h+1):
            for j in range(self.w):
                color = BLACK_SQUARE_COLOR if (i+j)%2 == 1 else WHITE_SQUARE_COLOR
                
                pyg.draw.rect(scr, color, (j*self.sq_w, i*self.sq_h, self.sq_w, self.sq_w))
        
        for piece in self.pieces:
            piece.draw(scr, self.sq_w, self.sq_h)
            
    def update(self):
        self.board = [[None for i in range(self.w)] for j in range(self.h)]
        for piece in self.pieces:
            self.set_to(piece)