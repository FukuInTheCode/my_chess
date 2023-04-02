from base_game import Game
import chess.pgn as chess
from os.path import isdir, isfile
from os import listdir
import random
import pickle

random.seed()

class OpeningPuzzle(Game):
    def __init__(self, scr_w: int, scr_h: int) -> None:
        self.score = 0
        self.did = 0 
        super().__init__(scr_w, scr_h)
        self.name = 'Puzzle Openings'

        
    def init(self):
        super().init()
        
        
        
        self.get_boards()
        
        print(self.type)
        
        self.load_data()
        
        self.did += 1

        self.needed = random.randint(1, len(self.boards)-1)
        
        self.is_turn = (-1)**(self.needed-1)
        
        self.board = self.boards[self.needed-1]

        self.needed = self.boards[self.needed]
        
        self.needed.print()

    def get_opening(self) -> tuple[str, tuple[str, str]]:
        path = "./PGN"

        folders = list(filter(lambda x: isdir(f"{path}\\{x}"), listdir(path)))
        op_type = random.choice(folders)
        
        path += "/" + op_type
        
        files = list(filter(lambda x: isfile(f"{path}\\{x}"), listdir(path)))
        
        op_variation = random.choice(files)
        
        self.type = (op_type, op_variation)
        
        return path + "/" + op_variation
        
    def get_boards(self):
        
        path= self.get_opening()
        
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

        
    def leftclick(self, mx: int, my: int) -> None:
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
        if self.board.compare(self.needed):
            self.score += 1
            
        print(self.type, self.score, self.did)
        
        self.save_data()
        
        self.init()

        
    def save_data(self):
        try:
            with open('opdata.pickle', "rb") as f:
                data = pickle.load(f)
                
            if self.type[0] in data.keys():
                if self.type[1] in data[self.type[0]].keys():
                    data[self.type[0]][self.type[1]][0] = self.score
                    data[self.type[0]][self.type[1]][1] = self.did
                        
                else:
                    data[self.type[0]][self.type[1]] = [self.score, self.did]
                    
            else:
                data[self.type[0]] = {
                    self.type[1]: [self.score, self.did]
                }
            
            print('save', data)
            
                
            with open("opdata.pickle", "wb") as f:
                pickle.dump(data, f, protocol=pickle.HIGHEST_PROTOCOL)
                
        except Exception as ex:
            print("Error during pickling object (Possibly unsupported):", ex)

        
        
    def load_data(self):
        try:
            with open('opdata.pickle', "rb") as f:
                data = pickle.load(f)
                print('load', data)
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