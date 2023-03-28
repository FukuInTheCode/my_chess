from copy import deepcopy

class P:
    def __init__(self) -> None:
        self.H = 10
        
        
l = [P()]

for i in l:
    print(i.H)

ll = deepcopy(l)

for i in ll:
    print(i.H)
    
ll[0].H = 2    

for i in l:
    print(i.H)
    

for i in ll:
    print(i.H)