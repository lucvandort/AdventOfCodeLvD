# -*- coding: utf-8 -*-

import matplotlib.pyplot as plt

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
    
#2nd exercise: 1 santa and 1 robotsanta take turns to deliver presents.
    
#%% figure route

def plot_route(route_coordinates):
    fig = plt.figure()
    ax = plt.subplot(1,1,1)
    
    x,y = list(zip(*route_coordinates))
    ax.plot(x,y)
        
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
        
route_coordinates = get_route_coordinates(inputcode)
present_count = get_present_count(route_coordinates)
num_coordinates = len(present_count)
plot_route(route_coordinates)