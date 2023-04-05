from base_game import Game
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
        
        self.buttons = {
            'redo': {
                'center': (self.w*0.9, self.h//18 + self.h),
                'radius': self.h//42,
                'color': (255, 0, 0)
            },
            'next': {
                'center': (self.w*0.8, self.h//18 + self.h),
                'radius': self.h//42,
                'color': (0, 255, 0)
            }
        }
        

    def init(self):
        super().init()

        self.is_turn = -1
        
        self.get_boards()
        self.needed = random.choice(range(2, len(self.boards), 2))
        self.boards[self.needed].print()
        self.board = self.boards[self.needed - 1]
        
        self.load_data()
        
        self.did += 1
    
    def get_boards(self):
        
        path = self.get_opening()
        
        file = open(path, 'r')
        pgn = chess.read_game(file)
        
        self.boards = [self.board.copy()]
        
        for move in pgn.mainline_moves():
            move = str(move)
            board = self.boards[-1].copy()
            board.move(*(ord(move[:2][0])-96, int(move[:2][1])), *(ord(move[2:][0])-96, int(move[2:][1])))
            board.update()
            self.boards.append(board)

        file.close()



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
                
    def check_puzzle(self):
        if self.board.compare(self.boards[self.needed]):
            self.score += 1
        
        self.is_waiting = True
            
        self.save_data()
    
    def subgame(self, mx, my):
        
        if not self.is_waiting:
            return
        
        def dist(p1, p2):
            return ((p1[0]-p2[0])**2 + (p1[1]-p2[1])**2)**(1/2)



        if dist((mx, my), self.buttons['next']['center']) <= self.buttons['next']['radius']:
            self.is_waiting = False
            self.init()

        
    def save_data(self):
        try:
            with open('opdata.pickle', "rb") as f:
                data = pickle.load(f)
                
            if self.type[0] in data[self.is_turn].keys():
                if self.type[1] in data[self.is_turn][self.type[0]].keys():
                    data[self.is_turn][self.type[0]][self.type[1]][0] = self.score
                    data[self.is_turn][self.type[0]][self.type[1]][1] = self.did
                        
                else:
                    data[self.is_turn][self.type[0]][self.type[1]] = [self.score, self.did]
                    
            else:
                data[self.is_turn][self.type[0]] = {
                    self.type[1]: [self.score, self.did]
                }
            
                
            with open("opdata.pickle", "wb") as f:
                pickle.dump(data, f, protocol=pickle.HIGHEST_PROTOCOL)
                
        except Exception as ex:
            print("Error during pickling object (Possibly unsupported):", ex)

        
        
    def load_data(self):
        try:
            with open('opdata.pickle', "rb") as f:
                data = pickle.load(f)[self.is_turn]
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
        font = pygame.font.Font('freesansbold.ttf', int(self.w//(len(self.type[0]) + len(self.type[1]) + 6 )))
        text = font.render(f'{self.type[0]}, {self.type[1]} : {round(self.score/self.did * 100, 2)}%', True, GREEN, BLUE)
        textRect = text.get_rect()
        textRect.topleft = (0, self.h)
        scr.blit(text, textRect)