# -*- coding: utf-8 -*-

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
            y_pos -= 1
        position_log.append((x_pos,y_pos))
        
    return position_log
        
def get_present_count(route_coordinates):
    present_count = {
        #(x,y): N       
    }    
    
    # hier moet dus iets dat het aantal kadootjes op elk coordinaat gaat tellen.

    return present_count
    
            

#%%
testinput = {
    ">": 2,
    "^>v<": 4,
    "^v^v^v^v^v": 2,
}

route_coordinates = get_route_coordinates("^v^v^><<>><v^v^v")
present_count = get_present_count(route_coordinates)
