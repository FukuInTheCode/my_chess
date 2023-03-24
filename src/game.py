import math
import pygame as pyg
from objects import Pawn, Queen

class Game():
    
    BASESIZE = (8, 8)
    
    WHITE_SQUARE = (238, 238, 210)
    
    BLACK_SQUARE = (118, 150, 86)
    
    def __init__(self, engine) -> None:
        self.engine = engine
        
        self.board = [[None for i in range(self.BASESIZE[0])] for _ in range(self.BASESIZE[1])]
        
        self.pieces = []
        
        self.tmp_w, self.tmp_h = self.engine.screen.get_size()
        self.square_size_w = self.tmp_w/self.BASESIZE[0]
        self.square_size_h = self.tmp_h/self.BASESIZE[1]
        
        self.hovered = None

        self.setupbase_pieces()
    
    def setupbase_pieces(self) -> None:

        self.pieces.append(Queen(self, 2, 2, True))
        
        self.pieces.append(Pawn(self, 2, 5, True))
        
        for piece in self.pieces:
            self.board[piece.y][piece.x] = piece

        self.update()
    
    def update(self) -> None:
        for piece in self.pieces:
            piece.setPossibleMoves()
    
    def draw(self) -> None:
        
        for i in range(self.BASESIZE[0]):
            for sq in range(self.BASESIZE[1]):
                pyg.draw.rect(self.engine.screen, (self.BLACK_SQUARE if sq%2 == i%2 else self.WHITE_SQUARE), (self.square_size_w*sq, self.tmp_h-(i+1)*self.square_size_h, self.square_size_w, self.square_size_h))

        for piece in self.pieces:
            piece.draw(self.square_size_w, self.square_size_h, self.tmp_h)
            
        if self.hovered is not None:
            for dx, dy in self.hovered.get_moves():
                pyg.draw.circle(self.engine.screen, (0, 0, 0), ((self.hovered.x + dx + 1/2)*self.square_size_w, (self.hovered.y + dy + 1/2)*self.square_size_h), min(self.square_size_w, self.square_size_h)//8)