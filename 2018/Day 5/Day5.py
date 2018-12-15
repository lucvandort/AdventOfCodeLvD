from array import array

with open('input.txt') as inputfile:
    inputstring = inputfile.readline().strip("\n")
    
char_array = array('u', inputstring)
#char_array = array('u', 'dabAcCaCBAcCcaDA')
    
# %%
    
    
length = len(char_array)
c = 0
i = 0
num_reactions = 1

while num_reactions > 0:
    print(f"# Iteration {i}")
    num_reactions = 0
    while c<len(char_array)-1:
        c1 = char_array[c]
        c2 = char_array[c+1]
#        print(f"Character {c} and {c+1}: {c1}{c2}")
        
        if (c1.islower() and c2.isupper() and c2.lower() == c1) or \
            (c1.isupper() and c2.islower() and c2.upper() == c1):
            print(f"Match char {c} and char {c+1}: {c1}{c2}")
            char_array.pop(c+1)
            char_array.pop(c)
            num_reactions += 1
        else:
            c += 1
    print(f"Number of reactions in iteration {i}: {num_reactions}")
    print(f"Remaining inputstring length: {len(char_array)}")
    i += 1
    c = 0

remaining_string = char_array.tounicode()