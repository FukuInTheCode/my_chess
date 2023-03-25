import pygame as pyg
import os


class Pawn():
    def __init__(self, game, x: int, y:int, t: bool) -> None:
        self.name = 'P'
        self.game = game
        self.team = t # True is white and False is black
        self.x = x - 1
        self.y = self.game.BASESIZE[1] - y
        self.setPossibleMoves()
        self.setImage()
        self.point = 1
        self.last_move = (self.x, self.y)
            
            
    def setPossibleMoves(self, wK: bool = False) -> None:
        self.moves = []
        if self.team: # case if white piece
            
            if self.y != 0:
            
                if self.game.board[self.y - 1][self.x] is None:
                    self.moves.append((0, -1))
                    if self.y == 6 and self.game.board[self.y - 2][self.x] is None:
                        self.moves.append((0, -2))

                if self.x != self.game.BASESIZE[0] - 1:
                    if self.game.board[self.y - 1][self.x + 1] is not None and not self.game.board[self.y - 1][self.x + 1].team:
                        self.moves.append((1, -1))
                        
                    if self.y == 3 and self.game.board[self.y][self.x + 1] is not None and self.game.board[self.y][self.x + 1].name == 'P' and self.game.board[self.y][self.x + 1].last_move == (0, 2):
                        self.moves.append((1, -1))
                        
                if self.x != 0:
                    if self.game.board[self.y - 1][self.x - 1] is not None and not self.game.board[self.y - 1][self.x - 1].team:
                        self.moves.append((-1,-1))
                        
                    if self.y == 3 and self.game.board[self.y][self.x - 1] is not None and self.game.board[self.y][self.x - 1].name == 'P' and self.game.board[self.y][self.x - 1].last_move == (0, 2):
                        self.moves.append((-1, -1))


        else: # case if black piece
                        
            if self.y != self.game.BASESIZE[1]-1: 
            
                if self.game.board[self.y + 1][self.x] is None:
                    self.moves.append((0, 1))
                    if self.y == 1 and self.game.board[self.y + 2][self.x] is None:
                        self.moves.append((0, 2))

                if self.x != self.game.BASESIZE[0] - 1:
                    if self.game.board[self.y + 1][self.x + 1] is not None and self.game.board[self.y + 1][self.x + 1].team:
                        self.moves.append((1, 1))
                        
                    if self.y == self.game.BASESIZE[1]-4 and self.game.board[self.y][self.x + 1] is not None and self.game.board[self.y][self.x + 1].name == 'P' and self.game.board[self.y][self.x + 1].last_move == (0, -2):
                        self.moves.append((1, 1))
                    
                        
                if self.x != 0:
                    if self.game.board[self.y + 1][self.x - 1] is not None and self.game.board[self.y + 1][self.x - 1].team:
                        self.moves.append((-1, 1))
                        
                    if self.y == self.game.BASESIZE[1]-4 and self.game.board[self.y][self.x - 1] is not None and self.game.board[self.y][self.x - 1].name == 'P' and self.game.board[self.y][self.x - 1].last_move == (0, -2):
                        self.moves.append((-1, 1))
                        
                        

    def get_attacked_squares(self):
        return ([(self.x-1, self.y-1), (self.x+1, self.y-1)] if self.team else [(self.x-1, self.y+1), (self.x+1, self.y+1)]) if self.name == 'P' else self.get_moves(True, True)
                        
    def get_moves(self, full: bool = False, wK: bool = False) -> list:
        self.setPossibleMoves(wK)
        
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
            
    def set_pos(self, dx, dy):
        self.last_move = (dx, dy)
        print(self.last_move)
        self.x += dx
        self.y += dy
        self.setPossibleMoves()
        self.draw()
        
class Queen(Pawn):
    
    def __init__(self, game, x: int, y: int, t: bool) -> None:
        super().__init__(game, x, y, t)
        self.point = 9
        self.name = 'Q'
        
    def setPossibleMoves(self, wK: bool = False) -> None:
        self.moves = []
            
        ds = [(0, 1), (0, -1), (1, 0), (1, 1), (1, -1), (-1, 0), (-1, -1), (-1, 1)]
        for dx, dy in ds:
            tdx = 0
            tdy = 0
            
            tdx += dx
            tdy += dy
            while 0 <= self.x + tdx < self.game.BASESIZE[0] and 0<=self.y + tdy<self.game.BASESIZE[1] and (self.game.board[self.y + tdy][self.x + tdx] is None or self.game.board[self.y + tdy][self.x + tdx].team != self.team):
                self.moves.append((tdx, tdy))
                if self.game.board[self.y + tdy][self.x + tdx] is not None and self.game.board[self.y + tdy][self.x + tdx].name == 'K' and wK:
                    tdx += dx
                    tdy += dy
                    continue
                if self.game.board[self.y + tdy][self.x + tdx] is not None:
                    break
                tdx += dx
                tdy += dy
                
            if 0 <= self.x + tdx < self.game.BASESIZE[0] and 0<=self.y + tdy<self.game.BASESIZE[1] and wK:
                self.moves.append((tdx, tdy))
                
    
    def setImage(self) -> None:
        if self.team:
            self.image = pyg.image.load('assets\whitepiece\whiteQueen.png')
        else:
            self.image = pyg.image.load('assets/blackpiece/blackQueen.png')
            
            
class Rook(Pawn):
    def __init__(self, game, x: int, y: int, t: bool) -> None:
        super().__init__(game, x, y, t)
        self.point = 5
        self.name = 'R'
        
    def setPossibleMoves(self, wK: bool = False) -> None:
        self.moves = []
        
        ds = [(0, 1), (0, -1), (1, 0), (-1, 0)]
        for dx, dy in ds:
            tdx = 0
            tdy = 0
            
            tdx += dx
            tdy += dy
            while 0 <= self.x + tdx < self.game.BASESIZE[0] and 0<=self.y + tdy<self.game.BASESIZE[1] and (self.game.board[self.y + tdy][self.x + tdx] is None or self.game.board[self.y + tdy][self.x + tdx].team != self.team):
                self.moves.append((tdx, tdy))
                if self.game.board[self.y + tdy][self.x + tdx] is not None and self.game.board[self.y + tdy][self.x + tdx].name == 'K' and self.game.board[self.y + tdy][self.x + tdx].team != self.team and wK:
                    tdx += dx
                    tdy += dy
                    continue
                if (self.game.board[self.y + tdy][self.x + tdx] is not None and self.game.board[self.y + tdy][self.x + tdx].team != self.team):
                    break
                tdx += dx
                tdy += dy
                
                            
            if 0 <= self.x + tdx < self.game.BASESIZE[0] and 0<=self.y + tdy<self.game.BASESIZE[1] and wK:
                self.moves.append((tdx, tdy))
                
    def setImage(self) -> None:
        if self.team:
            self.image = pyg.image.load('assets\whitepiece\whiteRook.png')
        else:
            self.image = pyg.image.load('assets/blackpiece/blackRook.png')
            
            
class Bishop(Pawn):
    def __init__(self, game, x: int, y: int, t: bool) -> None:
        super().__init__(game, x, y, t)
        self.point = 3
        self.name = 'B'
        
    def setPossibleMoves(self, wK: bool = False) -> None:
        self.moves = []
        
        ds = [(1, 1), (1, -1), (-1, -1), (-1, 1)]
        for dx, dy in ds:
            tdx = 0
            tdy = 0
            
            tdx += dx
            tdy += dy
            while 0 <= self.x + tdx < self.game.BASESIZE[0] and 0<=self.y + tdy<self.game.BASESIZE[1] and (self.game.board[self.y + tdy][self.x + tdx] is None or self.game.board[self.y + tdy][self.x + tdx].team != self.team):
                self.moves.append((tdx, tdy))
                if self.game.board[self.y + tdy][self.x + tdx] is not None and self.game.board[self.y + tdy][self.x + tdx].name == 'K' and self.game.board[self.y + tdy][self.x + tdx].team != self.team and wK:
                    tdx += dx
                    tdy += dy
                    continue
                if (self.game.board[self.y + tdy][self.x + tdx] is not None and self.game.board[self.y + tdy][self.x + tdx].team != self.team):
                    break
                tdx += dx
                tdy += dy
            
                            
            if 0 <= self.x + tdx < self.game.BASESIZE[0] and 0<=self.y + tdy<self.game.BASESIZE[1] and wK:
                self.moves.append((tdx, tdy))
                
    def setImage(self) -> None:
        if self.team:
            self.image = pyg.image.load('assets\whitepiece\whiteBishop.png')
        else:
            self.image = pyg.image.load('assets/blackpiece/blackBishop.png')
            
            
class Knight(Pawn):
    def __init__(self, game, x: int, y: int, t: bool) -> None:
        super().__init__(game, x, y, t)
        self.point = 3
        self.name = 'N'
        
    def setPossibleMoves(self, wK: bool = False) -> None:
        self.moves = []
        
        ds = [(1, 2), (2, 1), (2, -1), (1, -2), (-1, -2), (-2, -1), (-2, 1), (-1, 2)]
        
        for dx, dy in ds:
            
            if not (0<=self.x+dx<self.game.BASESIZE[0] and 0<=self.y+dy<self.game.BASESIZE[1]):
                continue
            
            if (self.game.board[self.y + dy][self.x + dx] is not None and self.game.board[self.y + dy][self.x + dx].team != self.team) or self.game.board[self.y + dy][self.x + dx] is None:
                self.moves.append((dx, dy))
                
            if wK:
                self.moves.append((dx, dy))
                
    def setImage(self) -> None:
        if self.team:
            self.image = pyg.image.load('assets\whitepiece\whiteKnight.png')
        else:
            self.image = pyg.image.load('assets/blackpiece/blackKnight.png')
            
            
class King(Pawn):
    def __init__(self, game, x: int, y: int, t: bool) -> None:
        super().__init__(game, x, y, t)
        self.point = 0
        self.name = 'K'
        
    def setPossibleMoves(self, wK: bool = False) -> None:
        self.moves = []
        
        ds = [(0, 1), (0, -1), (1, 0), (1, 1), (1, -1), (-1, 0), (-1, -1), (-1, 1)]
        
        if wK:
            self.moves = ds
            return
        
        for dx, dy in ds:
            
            if not (0<=self.x+dx<self.game.BASESIZE[0] and 0<=self.y+dy<self.game.BASESIZE[1]):
                continue
            
            if (self.game.board[self.y + dy][self.x + dx] is not None and self.game.board[self.y + dy][self.x + dx].team != self.team and self.game.board[self.y + dy][self.x + dx].name != 'K') or self.game.board[self.y + dy][self.x + dx] is None:
                tmp = True
                for piece in self.game.pieces:
                    if piece.team == self.team or piece is self:
                        continue
                    for move in piece.get_attacked_squares():
                        if move == (self.x + dx, self.y + dy):
                            tmp = False
                            break
                if tmp:
                    self.moves.append((dx, dy))
                
    def setImage(self) -> None:
        if self.team:
            self.image = pyg.image.load('assets\whitepiece\whiteKing.png')
        else:
            self.image = pyg.image.load('assets/blackpiece/blackKing.png')