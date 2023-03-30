import pygame as pyg
from CONSTANT import *
from board import Board

class Pawn:
    def __init__(self, x:int, y:int, team:int) -> None:
        self.x = x
        self.y = y
        self.team = int(team//abs(team))
        self.type = 'P'
        self.point = 1*self.team
        self.last_move = None
        
        self.set_image()
        
    def get_xy(self) -> tuple[int, int]:
        return (self.x, self.y)
    
    def get_possible_ds_moves(self)->list:
        tmp = []
        for dx, dy in PAWN_DXDY_MOVES(self.team):
            tmp.append((self.x + dx, self.y + dy))
            
        return tmp
            
    def get_faisable_position(self, board:Board)->list:
        moves = self.get_possible_ds_moves()
        
        tmp = []

        starting_pos = 7 if self.team == -1 else 2
        
        if board.check_xy(*moves[0]) and board.is_xy_none(*moves[0]):
            tmp.append(moves[0])
            
            if board.check_xy(*moves[1]) and self.y == starting_pos and board.is_xy_none(*moves[0]):
                tmp.append(moves[1])
                
        for m in (moves[2], moves[3]):
            
            print(board.get_xy(m[0], self.y).last_move) if board.get_xy(m[0], self.y) is not None else 0
                
            if board.check_xy(*m) and not board.is_xy_none(*m) and board.get_xy(*m).team != self.team:
                tmp.append(m)
                
            elif board.check_xy(*m) and board.is_xy_none(*m) and not board.is_xy_none(m[0], self.y) and board.get_xy(m[0], self.y).team != self.team and board.get_xy(m[0], self.y).type == self.type and board.get_xy(m[0], self.y).last_move == (0, 2*self.team*(-1)):
                tmp.append(m)
                
        return tmp
    
    def set_image(self):
        if self.team == 1:
            self.image = pyg.image.load('assets\whitepiece\whitePawn.png')
            
        else:
            self.image = pyg.image.load('assets/blackpiece/blackPawn.png')
            
        self.image = self.image.convert_alpha()
        
    
    def set_pos(self, x, y) -> None:
        self.last_move = (x - self.x, y - self.y)
        self.x = x
        self.y = y
        
                
    
    def draw(self, scr:pyg.Surface, sq_w, sq_h):
        self.image = pyg.transform.scale(self.image, (sq_w, sq_h))
        scr.blit(self.image, ((self.x-1)*sq_w, (self.y-1)*sq_h))
        

    def draw_moves(self, scr:pyg.Surface, board):
        for x, y in self.get_faisable_position(board):
            pyg.draw.circle(scr, GRAY, ((x - 1 + 1/2)*board.sq_w, (y - 1 + 1/2)*board.sq_h), min(board.sq_w, board.sq_h)//10)