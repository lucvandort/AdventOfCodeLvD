# -*- coding: utf-8 -*-

import re

#%% define functions    
def get_floornumber(code):
    open_tags = re.sub("\)",'',code)
    close_tags = re.sub("\(",'',code)
    floornumber = len(open_tags) - len(close_tags)
    return floornumber

def get_basement_position(code):
    floornumber_counter = [0]
    
    for c in code:
        if c is '(':
            floornumber_counter.append(floornumber_counter[-1] + 1)
        elif c is ')':
            floornumber_counter.append(floornumber_counter[-1] - 1)
        
        if floornumber_counter[-1] is -1:
            return len(floornumber_counter)-1
        
#%% test function floornumber
testcodes = {
    "(())": 0,
    "()()": 0,
    "(((": 3,
    "(()(()(": 3,
    "))(((((": 3,
    "())": -1,
    "))(": -1,
    ")))": -3,
    ")())())": -3,
}

for code, floornumber in testcodes.items():
    assert(get_floornumber(code)==floornumber)

#%% test function basement position
testcodes2 = {
    ")": 1,
    "()())": 5,
}

for code, position in testcodes2.items():
    assert(get_basement_position(code)==position)
    
#%% import input text
inputfile = open('input.txt')
inputcode = inputfile.read()

#%% answer part 1
floornumber = get_floornumber(inputcode)

#%% answer part 2
basement_charater_position = get_basement_position(inputcode)
