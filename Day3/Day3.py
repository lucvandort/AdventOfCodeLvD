# -*- coding: utf-8 -*-

import matplotlib.pyplot as plt
import pandas as pd

plt.close('all')

#%% 

def get_route_coordinates(inputcommands):
    x_pos = 0    
    y_pos = 0
    position_log = [(x_pos,y_pos)]
    
    for c in inputcommands:
        if c is "^":
            y_pos += 1
        elif c is "v":
            y_pos -= 1
        elif c is ">":
            x_pos += 1
        elif c is "<":
            x_pos -= 1
        position_log.append((x_pos,y_pos))
        
    return position_log
        
def get_present_count(route_coordinates):
    present_count = {
        #(x,y): N       
    }    
    
    for coordinate in route_coordinates:
        try:
            present_count[coordinate] += 1
        except KeyError:
            present_count[coordinate] = 1

    return present_count
    
    
#%% figure route

def plot_route(route_coordinates, route_coordinates2=None):
    fig = plt.figure()
    ax = plt.subplot(1,1,1)
    
    x,y = list(zip(*route_coordinates))
    ax.plot(x,y,'b')
    
    if route_coordinates2:
        x2,y2 = list(zip(*route_coordinates2))
        ax.plot(x2,y2,'r')
        
    fig.tight_layout()

#%%
testinput = {
    ">": 2,
    "^>v<": 4,
    "^v^v^v^v^v": 2,
}

for inputstring, houses in testinput.items():    
    route_coordinates = get_route_coordinates(inputstring)
    present_count = get_present_count(route_coordinates)
    num_coordinates = len(present_count)
    assert(houses == num_coordinates)

#%% import data

with open('input.txt', 'r') as inputfile:
    inputcode = inputfile.read()    
   
#%% part 1
     
route_coordinates = get_route_coordinates(inputcode)
present_count = get_present_count(route_coordinates)
num_coordinates = len(present_count)
plot_route(route_coordinates)

#%% part 2

inputcode_even = inputcode[0::2]
inputcode_odd = inputcode[1::2]

route_coordinates1 = get_route_coordinates(inputcode_even)
route_coordinates2 = get_route_coordinates(inputcode_odd)
plot_route(route_coordinates1, route_coordinates2)

present_count1 = pd.DataFrame.from_dict(get_present_count(route_coordinates1), orient='index')
present_count1.columns = ['Santa']
present_count2 = pd.DataFrame.from_dict(get_present_count(route_coordinates2), orient='index')
present_count2.columns = ['Robo Santa']

present_count_total = pd.merge(present_count1, present_count2, how='outer', left_index=True, right_index=True)
present_count_total = present_count_total.fillna(0)
present_count_total['Total'] = present_count_total['Santa'] + present_count_total['Robo Santa']
num_coordinates2 = len(present_count_total)