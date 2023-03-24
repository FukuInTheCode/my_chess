import pygame as pyg
import os


class Pawn():
    def __init__(self, game, x: int, y:int, t: bool) -> None:
        self.game = game
        self.team = t # True is white and False is black
        self.x = x - 1
        self.y = self.game.BASESIZE[1] - y
        self.setPossibleMoves()
        self.setImage()
        self.point = 1
            
            
    def setPossibleMoves(self) -> None:
        self.moves = []
        if self.team: # case if white piece
            
            if self.y != 7:
            
                if self.game.board[self.y + 1][self.x] is None:
                    self.moves.append((0, 1))
                    if self.y == 1 and self.game.board[self.y + 2][self.x] is None:
                        self.moves.append((0, 2))

                if self.x != 7:
                    if self.game.board[self.y + 1][self.x + 1] is not None and not self.game.board[self.y + 1][self.x + 1].team:
                        self.moves.append((1, 1))
                        
                if self.x != 0:
                    if self.game.board[self.y + 1][self.x - 1] is not None and not self.game.board[self.y + 1][self.x - 1].team:
                        self.moves.append((-1, 1))
            
        else: # case if black piece
                        
            if self.y != 0:
            
                if self.game.board[self.y - 1][self.x] is None:
                    self.moves.append((0, -1))
                    if self.y == 6 and self.game.board[self.y - 2][self.x] is None:
                        self.moves.append((0, -2))

                if self.x != 7:
                    if self.game.board[self.y - 1][self.x + 1] is not None and self.game.board[self.y - 1][self.x + 1].team:
                        self.moves.append((1, -1))
                        
                if self.x != 0:
                    if self.game.board[self.y - 1][self.x - 1] is not None and self.game.board[self.y - 1][self.x - 1].team:
                        self.moves.append((-1, -1))
                        
                        
    def get_moves(self, full: bool = False) -> tuple:
        self.setPossibleMoves()
        if full:
            return [(self.x + dx, self.y + dy) for dx, dy in self.moves]
        
        return self.moves
    
    def draw(self) -> None:
        self.image = pyg.transform.scale(self.image, (self.game.square_size_w, self.game.square_size_h)).convert_alpha()
        self.game.engine.screen.blit(self.image, (self.x*self.game.square_size_w, self.y*self.game.square_size_h))
        
        
    def setImage(self) -> None:
        if self.team:
            self.image = pyg.image.load('assets\whitepiece\whitePawn.png')
        else:
            self.image = pyg.image.load('assets/blackpiece/blackPawn.png')
            
    def set_pos(self, x, y):
        self.x = x
        self.y = y
        self.setPossibleMoves()
        self.draw()
        
        
class Queen(Pawn):
    
    def __init__(self, game, x: int, y: int, t: bool) -> None:
        super().__init__(game, x, y, t)
        self.point = 9
        
    def setPossibleMoves(self) -> None:
        self.moves = []
            
        ds = [(0, 1), (0, -1), (1, 0), (1, 1), (1, -1), (-1, 0), (-1, -1), (-1, 1)]
        for dx, dy in ds:
            tdx = 0
            tdy = 0
            
            tdx += dx
            tdy += dy
            while 0 <= self.x + tdx < self.game.BASESIZE[0] and 0<=self.y + tdy<self.game.BASESIZE[1] and (self.game.board[self.y + tdy][self.x + tdx] is None or self.game.board[self.y + tdy][self.x + tdx].team != self.team):
                self.moves.append((tdx, tdy))
                if (self.game.board[self.y + tdy][self.x + tdx] is not None and self.game.board[self.y + tdy][self.x + tdx].team != self.team):
                    break
                tdx += dx
                tdy += dy
            
    
    def setImage(self) -> None:
        if self.team:
            self.image = pyg.image.load('assets\whitepiece\whiteQueen.png')
        else:
            self.image = pyg.image.load('assets/blackpiece/blackQueen.png')