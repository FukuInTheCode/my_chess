from os.path import isdir, getsize
from os import listdir

def size_getting(path: str = './') -> int:
    size = 0
    for contained in listdir(path):
        if isdir(path + "/" + contained):
            size += size_getting(path + "/" + contained)
        
        else:
            size += getsize(path + "/" + contained)
            
    return size