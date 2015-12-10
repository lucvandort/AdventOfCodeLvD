# -*- coding: utf-8 -*-

#==============================================================================
# --- Day 2: I Was Told There Would Be No Math ---
# 
# The elves are running low on wrapping paper, and so they need to submit an order for more. They have a list of the dimensions (length l, width w, and height h) of each present, and only want to order exactly as much as they need.
# 
# Fortunately, every present is a box (a perfect right rectangular prism), which makes calculating the required wrapping paper for each gift a little easier: find the surface area of the box, which is 2*l*w + 2*w*h + 2*h*l. The elves also need a little extra paper for each present: the area of the smallest side.
# 
# For example:
# 
# A present with dimensions 2x3x4 requires 2*6 + 2*12 + 2*8 = 52 square feet of wrapping paper plus 6 square feet of slack, for a total of 58 square feet.
# A present with dimensions 1x1x10 requires 2*1 + 2*10 + 2*10 = 42 square feet of wrapping paper plus 1 square foot of slack, for a total of 43 square feet.
# All numbers in the elves' list are in feet. How many total square feet of wrapping paper should they order?
#==============================================================================

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
    
#%% import data
    
total_square_feet = 0
with open('input.txt', 'r') as inputfile:
    for inputstring in inputfile:
        dimensions = get_dimensions(inputstring)
        surface = get_square_feet(dimensions)
        total_square_feet += surface


