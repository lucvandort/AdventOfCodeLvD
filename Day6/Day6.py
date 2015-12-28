import re
import pandas as pd
import numpy as np

#%% definitions

def process_commands(data):
    
    p = re.compile('(?P<com>[a-z ]*) (?P<x1>\d+),(?P<y1>\d+) through (?P<x2>\d+),(?P<y2>\d+)')
    def rowprocessor(row):    
        searchresults = re.match(p, row['Inputstring']).groups()
        row[['com', 'x1', 'y1', 'x2', 'y2']] = searchresults
        return row

    data = data.apply(rowprocessor, axis = 1)
    data.loc[:][['x1', 'y1', 'x2', 'y2']] = data.loc[:][['x1', 'y1', 'x2', 'y2']].astype(int)
            
    return data
  
def calculate_lights(commands, gridsize=1000):
    grid = np.zeros((gridsize,gridsize), dtype=bool)
    
    for index in commands.index:
        raw, com, x1, y1, x2, y2 = commands.loc[index]
        if com == 'turn on':
            grid[x1:x2+1,y1:y2+1] = True
        elif com == 'turn off':
            grid[x1:x2+1,y1:y2+1] = False
        elif com == 'toggle':
            grid[x1:x2+1,y1:y2+1] = np.logical_not(grid[x1:x2+1,y1:y2+1])
        
    return grid
    
def calculate_light_intensity(commands, gridsize=1000):
    grid = np.zeros((gridsize,gridsize), dtype=int)
    
    for index in commands.index:
        raw, com, x1, y1, x2, y2 = commands.loc[index]
        if com == 'turn on':
            grid[x1:x2+1,y1:y2+1] += 1
        elif com == 'turn off':
            grid[x1:x2+1,y1:y2+1] -= 1
            grid[grid < 0] = 0
        elif com == 'toggle':
            grid[x1:x2+1,y1:y2+1] += 2
        
    return grid
    
    
COMMAND_COLUMNS = ['Inputstring', 'com', 'x1', 'y1', 'x2', 'y2']

    
#%% testing
    
testcommands = pd.DataFrame(index=range(3), columns=COMMAND_COLUMNS)

#                     ('raw', com', x1, y1, x2, y2)
testcommands.loc[0] = (None, 'turn on', 1, 3, 2, 4)
testcommands.loc[1] = (None, 'toggle', 1, 1, 3, 4) 
testcommands.loc[2] = (None, 'turn off', 2, 2, 2, 4)
testcommands.loc[3] = (None, 'turn off', 4, 4, 4, 4)

testgrid = calculate_lights(testcommands, gridsize=5)
testgrid2 = calculate_light_intensity(testcommands, gridsize=5)
    
#%% read input

with open('input.txt', 'r') as inputfile:
    inputstrings = [line[:-1] for line in inputfile]
    
commands = pd.DataFrame(index=range(len(inputstrings)), columns=COMMAND_COLUMNS)
commands['Inputstring'] = inputstrings    
    
#%% 
    
commands = process_commands(commands)

grid = calculate_lights(commands)
num_lights = np.count_nonzero(grid)

grid_intensities = calculate_light_intensity(commands)
total_intensity = grid_intensities.sum()

