from base_game import Game, Button
import chess.pgn as chess
from os.path import isdir, isfile
from os import listdir
import random
from CONSTANT import *
import pickle
import pygame as pyg
from generate_pickle import ls, save_object


random.seed()

pygame.init()

class OpeningPuzzle(Game):
    def __init__(self, scr_w: int, scr_h: int) -> None:
        self.score = 0
        self.did = 0
        self.is_waiting = False
        
        
        if 'opdata.pickle' not in listdir('./'):
            save_object(ls)
        
        super().__init__(scr_w, scr_h)
        self.name = 'Puzzle Openings'
        
        self.buttons = [
            Button(self.w*0.9, self.h//18 + self.h, self.h//42, (0, 255, 0), self.next),
            Button(self.w*0.8, self.h//18 + self.h, self.h//42, (255, 0, 0), self.redo),
            Button(self.w*0.7, self.h//18 + self.h, self.h//42, (255, 255, 0), self.see_answ)
        ]
        
        self.streak = 0
        

    def init(self):
        super().init()
        
        self.choice_board()

        if self.is_turn == 1:
            self.rotate()

        self.load_data()
    
    def get_boards(self, op):
        
        path = op
        
        file = open(path, 'r')
        pgn = chess.read_game(file)
        
        boards = [self.board.copy()]
        
        for move in pgn.mainline_moves():
            move = str(move)
            board = boards[-1].copy()
            board.move(*(ord(move[:2][0])-96, int(move[:2][1])), *(ord(move[2:][0])-96, int(move[2:][1])))
            board.update()
            boards.append(board)


        file.close()
        
        return boards



    def get_opening(self) -> tuple[str, tuple[str, str]]:
        path = "./PGN/White" if self.is_turn == 1 else "./PGN/Black"

        folders = list(filter(lambda x: isdir(f"{path}\\{x}"), listdir(path)))

        game_type = random.choice(folders)
        
        path += "/" + game_type
        
        folders = list(filter(lambda x: isdir(f"{path}\\{x}"), listdir(path)))
        op_type = random.choice(folders)
         
        path += "/" + op_type
        
        files = list(filter(lambda x: isfile(f"{path}\\{x}"), listdir(path)))
        
        op_variation = random.choice(files)
        
        self.type = (game_type, op_type)
        
        return path + "/" + op_variation
    
    
    def choice_board(self):
        self.is_turn = self.op_side = random.choice([1, -1])

        
        self.boards = self.get_boards(self.get_opening())
        
        
        
        path =( "./PGN/White" if self.is_turn == 1 else "./PGN/Black") + "/" +  self.type[0] + "/" +  self.type[1] + "/base"
        base = self.get_boards(path)
        
        if len(base) == len(self.boards):
            if self.is_turn == -1:
                self.needed = random.choice(range(2, len(self.boards), 2))
                
            else:
                self.needed = random.choice(range(1, len(self.boards), 2))
                
        else:
            if self.is_turn == -1:
                self.needed = random.choice(range(len(base)+1, len(self.boards), 2))
                
            else:
                self.needed = random.choice(range(len(base), len(self.boards), 2))
            
        
        self.board = self.boards[self.needed - 1].copy()

    
        
    def leftclick(self, mx: int, my: int) -> None:
        
        if self.is_waiting:
            return
        
        mx = mx//self.board.sq_w + 1
        my = my//self.board.sq_h + 1
        
        tmp = self.clicked
        
        self.clicked = self.board.get_xy(mx, my)
        
        if self.clicked is not None and self.clicked.team != self.is_turn:
            self.clicked = None

        if tmp is not None and (mx, my) in tmp.get_faisable_position(self.board) and not self.board.in_check(*tmp.get_xy(), mx, my, tmp.team):
            self.board.move(*tmp.get_xy(), mx, my)
            self.clicked = None
            self.board.update()
                        
            if self.board.in_checkmate(self.is_turn):
                self.checkmate(self.is_turn*-1)
                
            self.check_puzzle()
                
        
    def save_data(self):
        try:
            with open('opdata.pickle', "rb") as f:
                data = pickle.load(f)
            
            if self.type[0] in data[self.op_side].keys():
                if self.type[1] in data[self.op_side][self.type[0]].keys():
                    
                    data[self.op_side][self.type[0]][self.type[1]][0] = self.score
                    data[self.op_side][self.type[0]][self.type[1]][1] = self.did
                        
                else:
                    data[self.op_side][self.type[0]][self.type[1]] = [self.score, self.did]
                    
            else:
                data[self.op_side][self.type[0]] = {
                    self.type[1]: [self.score, self.did]
                }
            
                
            with open("opdata.pickle", "wb") as f:
                pickle.dump(data, f, protocol=pickle.HIGHEST_PROTOCOL)
                
        except Exception as ex:
            print("Error during pickling object (Possibly unsupported):", ex)

        
        
    def load_data(self):
        try:
            with open('opdata.pickle', "rb") as f:
                data = pickle.load(f)[self.op_side]
                if self.type[0] in data.keys():
                    data = data[self.type[0]]
                    if self.type[1] in data.keys():
                        data = data[self.type[1]]
                        self.score = data[0]
                        self.did = data[1]
                        return
                        
                
                self.score = 0
                self.did = 0
                
        except Exception as ex:
            print("Error during unpickling object (Possibly unsupported):", ex)
            
    
    def draw(self, scr: pyg.Surface) -> None:
        super().draw(scr)
        txts = [
            f'{self.type[0]}, {self.type[1]} : {round(self.score/(self.did if self.did != 0 else 1) * 100, 2)}%',
            f'Current streak: {self.streak}'
        ]
        tmp = 0
        for txt in txts:
            font = pygame.font.Font('freesansbold.ttf', int(self.w//len(txt)))
            text = font.render(txt, True, GREEN, BLUE)
            textRect = text.get_rect()
            textRect.topleft = (0, self.h + tmp)
            tmp = textRect.h+(self.h/0.9)*0.01
            scr.blit(text, textRect)
            
    def rotate(self):
        super().rotate()
        for bd in self.boards:
            bd.rotate()
            
    def check_puzzle(self):
        if self.board.compare(self.boards[self.needed]):
            self.score += 1

            self.streak += 1
            
        else:
            self.streak = 0
        
        self.is_waiting = True
        
        self.did += 1
            
        self.save_data()
        
        
    def subgame(self, mx, my):
        
        if not self.is_waiting:
            return


        for btn in self.buttons:
            btn.check(mx, my)
        
    def next(self):
        self.is_waiting = False
        self.init()
        
    def redo(self):
        self.is_waiting = False
        self.board = self.boards[self.needed-1].copy()
        self.streak = 0
        
    def see_answ(self):
        self.board = self.boards[self.needed].copy()
        
