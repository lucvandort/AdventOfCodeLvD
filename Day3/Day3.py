# -*- coding: utf-8 -*-

#%% 

def count_presents(inputcommands):
    present_counter = {(0,0): 1}
    position_log = [(0,0)]
    
    for c in inputcommands:
        if c is "^":
            position_log.append((position_log[-1][0],position_log[-1][1]+1))
        elif c is "v":
            position_log.append((position_log[-1][0],position_log[-1][1]-1))
        elif c is ">":
            position_log.append((position_log[-1][0]+1,position_log[-1][1]))
        elif c is "<":
            position_log.append((position_log[-1][0]-1,position_log[-1][1]))
        
        print(position_log[-1])
            

#%%
testinput = {
    ">": 2,
    "^>v<": 4,
    "^v^v^v^v^v": 2,
}


count_presents("^v^v^v^v^v")
