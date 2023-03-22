import pygame as pyg
import os


class Pawn():
    def __init__(self, game, x: int, y:int, t: bool) -> None:
        self.game = game
        self.team = t # True is white and False is black
        self.x = x
        self.y = y
        self.setPossibleMoves()
        
        if self.team:
            self.image = pyg.image.load('assets\whitepiece\whitePawn.png')
        else:
            self.image = pyg.image.load('assets/blackpiece/blackPawn.png')
            

        
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
                        
                        
    def get_moves(self) -> tuple:
        self.setPossibleMoves()
        return self.moves
    
    def draw(self, sq_w, sq_h, h) -> None:
        self.image = pyg.transform.scale(self.image, (sq_w, sq_h)).convert_alpha()
        self.game.engine.screen.blit(self.image, (self.x*sq_w, h - (1+self.y)*sq_h))