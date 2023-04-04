from engine import Engine
import pygame as pyg

def main() -> None:
    scr = pyg.display.set_mode((1000, 720))
    Engine(scr)
    
    
if __name__ == "__main__":
    main()
    