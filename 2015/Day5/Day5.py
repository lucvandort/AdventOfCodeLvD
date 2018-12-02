import pandas as pd
import re

#%% Definitions

VOWEL = "aeiou"
NAUGHTY = ["ab","cd","pq","xy"]

    
def check_three_vowels(inputstrings):
    return inputstrings.apply(lambda inputstring: sum([inputstring.count(x) for x in VOWEL]) >= 3)
    

def check_double_letter(inputstrings):
    return inputstrings.apply(lambda inputstring: True in [inputstring[x]==inputstring[x+1] for x in range(len(inputstring)-1)])
    

def check_naughty_substring(inputstrings):
    return inputstrings.apply(lambda inputstring: True in [naughty_string in inputstring for naughty_string in NAUGHTY])

def check_letter_repetition(inputstrings):
    p = re.compile('(?P<letter>[a-z])[a-z](?P=letter)')
    searchresults = [len(re.findall(p, inputstring)) for inputstring in inputstrings]
    return searchresults
    
def check_letter_double(inputstrings):
    p = re.compile('(?P<letters>[a-z]{2})[a-z]*(?P=letters)')
    searchresults = [len(re.findall(p, inputstring)) for inputstring in inputstrings]
    return searchresults
    
#%% Read input

with open('input.txt', 'r') as inputfile:
    inputstrings = [line[:-1] for line in inputfile]
    
    columns1 = ['Inputstring', 'Three vowels', 'Double letter', 'Naughty substring', 'Nice string']
    data1 = pd.DataFrame(index=range(len(inputstrings)), columns=columns1)
    data1['Inputstring'] = inputstrings
    
    columns2 = ['Inputstring', 'Double letter repeat', 'Single letter repeat', 'Nice string']
    data2 = pd.DataFrame(index=range(len(inputstrings)), columns=columns2)
    data2['Inputstring'] = inputstrings

#%% Part 1

data1['Three vowels'] = check_three_vowels(data1['Inputstring'])
data1['Double letter'] = check_double_letter(data1['Inputstring'])
data1['Naughty substring'] = check_naughty_substring(data1['Inputstring'])
data1['Nice string'] = data1.apply(lambda row: row['Three vowels'] and row['Double letter'] and not row['Naughty substring'], axis=1)

nice_string_count = len(data1['Inputstring'].where(data1['Nice string']).dropna())

#%% Part 2

data2['Single letter repeat'] = check_letter_repetition(data2['Inputstring'])
data2['Double letter repeat'] = check_letter_double(data2['Inputstring'])

data2['Nice string'] = data2.apply(lambda row: bool(row['Single letter repeat'] and row['Double letter repeat']), axis=1)

nice_string2_count = len(data2['Inputstring'].where(data2['Nice string']).dropna())

# SELECT `Inputstring` FROM `data2` WHERE `Nice string` = TRUE
