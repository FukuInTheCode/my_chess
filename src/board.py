import pygame as pyg
from CONSTANT import BLACK_SQUARE_COLOR, WHITE_SQUARE_COLOR
from copy import deepcopy
from pieces import Queen

class Board:
    def __init__(self, w:int, h:int, scr_w:int, scr_h:int) -> None:
        self.board = [[None for i in range(w)] for j in range(h)]
        self.w = w
        self.h = h
        self.sq_w = int(scr_w//w)
        self.sq_h = int(scr_h//h)
        
        self.scr_w = scr_w
        self.scr_h = scr_h
        
        self.last_moved = None
        
        self.pieces = []
        
    def get_xy(self, x:int, y:int):
        return self.board[y-1][x-1]
    
    def get_piece(self, type, team):
        tmp = []
        
        for piece in self.pieces:
            if piece.type == type and piece.team == team:
                tmp.append(piece)
        
        return tmp
    
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
        
        self.last_moved.has_moved = True
        
        if tmp is not None:
            self.pieces.remove(tmp)
            
        elif self.last_moved.type == 'P':
            if tox - x != 0:
                self.pieces.remove(self.get_xy(tox, y))
                
        if self.last_moved.type == 'P' and self.last_moved.y == (8 if self.last_moved.team == 1 else 1):
            q = Queen(*self.last_moved.get_xy(), self.last_moved.team)
            q.last_move = self.last_moved.last_move
            q.has_moved = self.last_moved.has_moved
            self.pieces.remove(self.last_moved)
            self.add(q)
            self.last_moved = q
            
            
                
        if self.last_moved.type == 'K' and (tox - x != 0 or tox - x != 1 or tox - x != -1):
            if tox - x == 2:
                for i in range(tox, self.w + 1):
                    if not self.check_xy(i, self.last_moved.y):
                        raise Exception('Trying to castle without a rook!')
                    
                    elif not self.is_xy_none(i, self.last_moved.y) and self.get_xy(i, self.last_moved.y).type == 'R' and not self.get_xy(i, self.last_moved.y).has_moved:
                        self.move(i, self.last_moved.y, tox - 1, toy)
                        break
                    
            if tox - x == -2:
                for i in range(tox, 0, -1):
                    if not self.check_xy(i, self.last_moved.y):
                        raise Exception('Trying to castle without a rook!')
                    
                    elif not self.is_xy_none(i, self.last_moved.y) and self.get_xy(i, self.last_moved.y).type == 'R' and not self.get_xy(i, self.last_moved.y).has_moved:
                        self.move(i, self.last_moved.y, tox + 1, toy)
                        break

    def check_xy(self, x, y)->bool:
        if (0<x<=self.w) and (0<y<=self.h):
            return True
        
        return False
    
    def draw(self, scr) -> None:
        
        for i in range(self.h):
            for j in range(self.w):
                color = BLACK_SQUARE_COLOR if (i+j)%2 == 1 else WHITE_SQUARE_COLOR
                
                pyg.draw.rect(scr, color, (j*self.sq_w, i*self.sq_h, self.sq_w, self.sq_w))
        
        for piece in self.pieces:
            piece.draw(scr, self.sq_w, self.sq_h)
            
    def update(self):
        self.board = [[None for i in range(self.w)] for j in range(self.h)]
        for piece in self.pieces:
            self.set_to(piece)
            
    def in_check(self, x, y, tox, toy, team) -> bool:
        tmp = self.copy()
        tmp.move(x, y, tox, toy)
        tmp.update()
        
        for piece in tmp.pieces:
            if piece.type == 'K' and piece.team == team:
                king = piece 
                break
        
        for piece in tmp.pieces:
            if piece.team != team:
                for m in piece.get_faisable_position(tmp):
                    if tmp.get_xy(*m) == king:
                        return True
                
        return False
    

    def in_checkmate(self, team):
        for piece in self.pieces:
            for m in piece.get_faisable_position(self):
                if piece.team == team:
                    if not self.in_check(*piece.get_xy(), *m, piece.team):
                        print(piece.get_xy(), m)
                        return False
                
        return True
        
    def copy(self):
        tmp = Board(self.w, self.h, self.scr_w, self.scr_h)
        for piece in self.pieces:
            tmp.add(piece.copy())
            
        tmp.update()
        
        return tmp
            
            
    def print(self):
        for line in self.board:
            for square in line:
                if square is None:
                    print(' ', end=' ')
                    
                else:
                    print(square.type, end=' ')
                    
            print()
            
    
    def compare(self, board):
        if self.w == board.w and self.h and board.h:
            for y in range(1, self.h + 1):
                for x in range(1, self.w+1):
                    if self.is_xy_none(x, y) != board.is_xy_none(x, y):
                        return False
                    
                    elif self.is_xy_none(x, y) and  board.is_xy_none(x, y):
                        continue
                    
                    elif self.get_xy(x, y).type != board.get_xy(x, y).type or self.get_xy(x, y).team != board.get_xy(x, y).team or self.get_xy(x, y).last_move != board.get_xy(x, y).last_move:
                        return False   
                    
            return True
        
        return False          