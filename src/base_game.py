from board import Board
import pygame as pyg
from CONSTANT import BASE_BOARD_HEIGHT, BASE_BOARD_WIDTH
from pieces import *

class Game:
    def __init__(self, scr_w:int, scr_h:int) -> None:
        self.board = Board(BASE_BOARD_WIDTH, BASE_BOARD_HEIGHT, scr_w, scr_h)
        self.name = 'Chess Game'
        self.clicked = None
        self.init_pieces()
        
    def init_pieces(self):
        self.board.add(Pawn(2, 2, 1))
        self.board.add(Pawn(1, 3, -1))
        self.board.add(Pawn(3, 4, -1))
        
        for piece in self.board.pieces:
            self.board.set_to(piece)
        
    def draw(self, scr:pyg.Surface) -> None:
        self.board.draw(scr)
        if self.clicked != None:
            self.clicked.draw_moves(scr, self.board)
        
    def rightclick(self, mx:int, my:int) -> None:
        mx = mx//self.board.sq_w + 1
        my = my//self.board.sq_h + 1
        
        tmp = self.clicked
        
        self.clicked = self.board.get_xy(mx, my)
        
        print(tmp, self.clicked)
        print(mx, my)
        
        if tmp is not None and (mx, my) in tmp.get_faisable_position(self.board):
            self.board.move(*tmp.get_xy(), mx, my)
            self.clicked = None
            self.board.update()