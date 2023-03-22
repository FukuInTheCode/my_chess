import math
import pygame as pyg
from objects import Pawn

class Game():
    
    BASESIZE = (8, 8)
    
    WHITE_SQUARE = (238, 238, 210)
    
    BLACK_SQUARE = (118, 150, 86)
    
    def __init__(self, engine) -> None:
        self.engine = engine
        
        self.board = [[None for i in range(self.BASESIZE[0])] for _ in range(self.BASESIZE[1])]
        
        self.pieces = []

        self.setupbase_pieces()
    
    def setupbase_pieces(self) -> None:
        for i in range(8):
            self.pieces.append(Pawn(self, i, 1, True))
            self.pieces.append(Pawn(self, i, 6, False))
        
        for piece in self.pieces:
            self.board[piece.y][piece.x] = piece
    
    def update(self) -> None:
        pass
    
    def draw(self) -> None:
        tmp_w, tmp_h = self.engine.screen.get_size()
        square_size_w = tmp_w/self.BASESIZE[0]
        square_size_h = tmp_h/self.BASESIZE[1]
        
        for i in range(self.BASESIZE[0]):
            for sq in range(self.BASESIZE[1]):
                pyg.draw.rect(self.engine.screen, (self.BLACK_SQUARE if sq%2 == i%2 else self.WHITE_SQUARE), (square_size_w*sq, tmp_h-(i+1)*square_size_h, square_size_w, square_size_h))

        for piece in self.pieces:
            piece.draw(square_size_w, square_size_h, tmp_h)