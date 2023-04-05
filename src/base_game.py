from board import Board
import pygame as pyg
from CONSTANT import BASE_BOARD_HEIGHT, BASE_BOARD_WIDTH
from pieces import *

class Game:
    def __init__(self, scr_w:int, scr_h:int) -> None:
        self.w, self.h = (min(scr_w, scr_h) for i in range(2))
        self.name = 'Chess Game'
        self.clicked = None
        self.is_turn = 1
        self.buttons = []
        self.init()
        
    def init(self):
        self.board = Board(BASE_BOARD_WIDTH, BASE_BOARD_HEIGHT, self.w, self.h)
        for i in range(1, 9):
            self.board.add(Pawn(i, 2, 1))
            self.board.add(Pawn(i, 7, -1))
        
        self.board.add(King(5, 1, 1))
        self.board.add(King(5, 8, -1))    
        
        self.board.add(Queen(4, 1, 1))
        self.board.add(Queen(4, 8, -1))
        
        self.board.add(Rook(1, 1, 1))
        self.board.add(Rook(1, 8, -1))
        self.board.add(Rook(8, 1, 1))
        self.board.add(Rook(8, 8, -1))
        
        self.board.add(Bishop(3, 1, 1))
        self.board.add(Bishop(6, 8, -1))
        self.board.add(Bishop(6, 1, 1))
        self.board.add(Bishop(3, 8, -1))
        
        self.board.add(Knight(2, 1, 1))
        self.board.add(Knight(7, 8, -1))
        self.board.add(Knight(7, 1, 1))
        self.board.add(Knight(2, 8, -1))
        
        for piece in self.board.pieces:
            self.board.set_to(piece)
        
    def draw(self, scr:pyg.Surface) -> None:
        self.board.draw(scr)
        if self.clicked != None:
            self.clicked.draw_moves(scr, self.board)
            
        for btn in self.buttons:
            btn.draw(scr)
        
    def leftclick(self, mx:int, my:int) -> None:
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
                
                
    def checkmate(self, winner):
        print('Winner is '+ ('White' if winner == 1 else 'Black'))
        
    
    def subgame(self):
        pass
    
    
    def rotate(self):
        self.board.rotate()
        self.is_turn *= -1
    
        
class Button():
    def __init__(self, x, y, radius, color, func) -> None:
        self.radius = radius
        self.x = x
        self.y = y
        self.func = func
        self.color = color
        
    def get_dist(self, px, py):
        return ((self.x-px)**2 + (self.y-py)**2)**(1/2)
    
    def check(self, px, py):
        if self.get_dist(px, py) <= self.radius:
            self.func()
            
    def draw(self, scr):
        pyg.draw.circle(scr, self.color, (self.x, self.y), self.radius)