import math
import pygame as pyg
from objects import Pawn, Queen

class Game():
    
    BASESIZE = (8, 8)
    
    WHITE_SQUARE = (238, 238, 210)
    
    BLACK_SQUARE = (118, 150, 86)
    
    def __init__(self, engine) -> None:
        self.engine = engine
        
        self.pieces = []
        
        self.board = [[None for i in range(self.BASESIZE[0])] for _ in range(self.BASESIZE[1])]
        
        self.tmp_w, self.tmp_h = self.engine.screen.get_size()
        self.square_size_w = self.tmp_w/self.BASESIZE[0]
        self.square_size_h = self.tmp_h/self.BASESIZE[1]
        
        self.clicked = None
        
        self.is_turn = True
        
        self.setupbase_pieces()
    
    def setupbase_pieces(self) -> None:

        self.pieces.append(Queen(self, 2, 2, False))
        
        self.pieces.append(Pawn(self, 2, 5, True))
        

        self.update()
    
    def update(self) -> None:
        
        self.board = [[None for i in range(self.BASESIZE[0])] for _ in range(self.BASESIZE[1])]
        
        for piece in self.pieces:
            self.board[piece.y][piece.x] = piece
        
        for piece in self.pieces:
            piece.setPossibleMoves()
    
    def draw(self) -> None:
        
        print(self.calc_points())
        
        for i in range(self.BASESIZE[0]):
            for sq in range(self.BASESIZE[1]):
                pyg.draw.rect(self.engine.screen, (self.BLACK_SQUARE if sq%2 == i%2 else self.WHITE_SQUARE), (self.square_size_w*i, self.tmp_h-(sq+1)*self.square_size_h, self.square_size_w, self.square_size_h))

        for piece in self.pieces:
            piece.draw()
            
        if self.clicked is not None and self.clicked.team == self.is_turn:
            for dx, dy in self.clicked.get_moves():
                pyg.draw.circle(self.engine.screen, (100, 100, 100), ((self.clicked.x + dx + 1/2)*self.square_size_w, (self.clicked.y + dy + 1/2)*self.square_size_h), min(self.square_size_w, self.square_size_h)//16)
                
    def calc_points(self):
        bpts, wpts = (0, 0)
        
        for piece in self.pieces:
            if piece.team:
                wpts += piece.point
            else:
                bpts += piece.point
        
        return wpts, bpts