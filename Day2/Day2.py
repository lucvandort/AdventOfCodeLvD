# -*- coding: utf-8 -*-

import re

#%% define functions

def get_dimensions(inputstring):
    p = re.compile('^(?P<l>\d+)x(?P<w>\d+)x(?P<h>\d+)$')
    searchresults = re.search(p, inputstring)
    
    try:
        dimensions = searchresults.groupdict()
    except AttributeError:
        return None
    
    for dimension, value in dimensions.items():
            dimensions[dimension] = int(value)
            
    return dimensions

def get_square_feet(dimensions):
    l = dimensions['l']
    w = dimensions['w']
    h = dimensions['h']
    
    s1 = l*w
    s2 = w*h
    s3 = h*l
    
    surface = 2*s1 + 2*s2 + 2*s3 + min(s1,s2,s3)
    
    return surface
    
def get_ribbon_length(dimensions):
    l = dimensions['l']
    w = dimensions['w']
    h = dimensions['h']
    
    l1 = 2*(l+w)
    l2 = 2*(w+h)
    l3 = 2*(h+l)
    
    volume = l*w*h
    
    length = min(l1,l2,l3) + volume
    
    return length
    

#%% test functions
testinput = {
    "2x3x4": 58,
    "1x1x10": 43,
    "29x13x26": 3276,
    "11x11x14\n": 979,
    "27x2x5\n": 408,
    "6x10x13": 596,
    "15x19x10": 1400,
}

surfaces = []

for inputstring, squarefeet in testinput.items():
    dimensions = get_dimensions(inputstring)
    surface = get_square_feet(dimensions)
    assert(squarefeet == surface)
    surfaces.append(surface)
    
assert(sum(testinput.values()) == sum(surfaces))
    
testinput2 = {
    "2x3x4": 34,
    "1x1x10": 14,
}

lengths = []

for inputstring, ribbonlength in testinput2.items():
    dimensions = get_dimensions(inputstring)
    length = get_ribbon_length(dimensions)
    assert(ribbonlength == length)
    lengths.append(length)    
    
assert(sum(testinput2.values()) == sum(lengths))
    
#%% import data
    
total_square_feet = 0
total_ribbon_length = 0
with open('input.txt', 'r') as inputfile:
    for inputstring in inputfile:
        dimensions = get_dimensions(inputstring)
        surface = get_square_feet(dimensions)
        length = get_ribbon_length(dimensions)
        total_square_feet += surface
        total_ribbon_length += length
