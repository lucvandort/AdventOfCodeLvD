import pandas as pd

#%% Definitions

VOWEL = "aeiou"
NAUGHTY = ["ab","cd","pq","xy"]

    
def check_three_vowels(inputstrings):
    return inputstrings.apply(lambda inputstring: sum([inputstring.count(x) for x in VOWEL]) >= 3)
    

def check_double_letter(inputstrings):
    return inputstrings.apply(lambda inputstring: True in [inputstring[x]==inputstring[x+1] for x in range(len(inputstring)-1)])
    

def check_naughty_substring(inputstrings):
    return inputstrings.apply(lambda inputstring: True in [naughty_string in inputstring for naughty_string in NAUGHTY])


#%% Read input

with open('input.txt', 'r') as inputfile:
    inputstrings = [line[:-1] for line in inputfile]
    columns = ['Inputstring', 'Three vowels', 'Double letter', 'Naughty substring', 'Nice string']
    data = pd.DataFrame(index=range(len(inputstrings)), columns=columns)
    data['Inputstring'] = inputstrings

#%% Process input

data['Three vowels'] = check_three_vowels(data['Inputstring'])
data['Double letter'] = check_double_letter(data['Inputstring'])
data['Naughty substring'] = check_naughty_substring(data['Inputstring'])
data['Nice string'] = data.apply(lambda row: row['Three vowels'] and row['Double letter'] and not row['Naughty substring'], axis=1)

nice_string_count = len(data['Inputstring'].where(data['Nice string']).dropna())
