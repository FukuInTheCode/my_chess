# =================================================
# Constants
# =================================================

BASE_BOARD_HEIGHT = 8
BASE_BOARD_WIDTH = 8

BLACK = (0, 0, 0)
GRAY = (169,169,169)

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