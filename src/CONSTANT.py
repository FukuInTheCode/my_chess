import pygame

# =================================================
# Constants
# =================================================

BASE_BOARD_HEIGHT = 8
BASE_BOARD_WIDTH = 8

BLACK = (0, 0, 0)
GRAY = (169,169,169)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
LIGHT_YELLOW = (247, 247, 105)
DARK_YELLOW = (187, 203, 43)
YELLOW = (255, 255, 0)
RED = (255, 0, 0)

BLACK_SQUARE_COLOR = (118, 150, 86)
WHITE_SQUARE_COLOR = (238, 238, 210)

# =================================================
# Pieces moves func
# =================================================

def PAWN_DXDY_MOVES(team:int):
    return [
    (0, 1*team),
    (0, 2*team),
    (1, 1*team),
    (-1, 1*team)
    ]
    
    
def QUEEN_DXDY_MOVES():
    return [
        (i, 0) for i in range(1, 8) ] + [
            (i, 0) for i in range(-1, -8, -1)
        ] + [
            (0, i) for i in range(1, 8)
        ] + [
            (0, i) for i in range(-1, -8, -1)
        ] + [
            (i, i) for i in range(1, 8)
        ] + [
            (i, i) for i in range(-1, -8, -1)
        ] + [
            (i, -i) for i in range(1, 8)
        ] + [
             (i, -i) for i in range(-1, -8, -1)
        ]
        

def ROOK_DXDY_MOVES():
    return [
        (i, 0) for i in range(1, 8) ] + [
            (i, 0) for i in range(-1, -8, -1)
        ] + [
            (0, i) for i in range(1, 8)
        ] + [
            (0, i) for i in range(-1, -8, -1)
        ]
        

def BISHOP_DXDY_MOVES():
    return [
            (i, i) for i in range(1, 8)
        ] + [
            (i, i) for i in range(-1, -8, -1)
        ] + [
            (i, -i) for i in range(1, 8)
        ] + [
             (i, -i) for i in range(-1, -8, -1)
        ]
        
def KNIGHT_DXDY_MOVES():
    return [
        (1, 2),
        (2, 1),
        (2, -1),
        (1, -2),
        (-1, -2),
        (-2, -1),
        (-2, 1),
        (-1, 2),
    ]
        
        
def KING_DXDY_MOVES():
    return [
        (1, 1),
        (0, 1),
        (1, 0), 
        (0, -1),
        (-1, 0),
        (1, -1),
        (-1, 1),
        (-1, -1)
    ]