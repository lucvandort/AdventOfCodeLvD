from array import array
import string
import pandas as pd

with open('input.txt') as inputfile:
    inputstring = inputfile.readline().strip("\n")

# %%


def react_polymer(inputstring, verbose=False):
    char_array = array('u', inputstring)
    c = 0
    i = 0
    num_reactions = 1

    while num_reactions > 0:
        if verbose:
            print(f"# Iteration {i}")
        elif i % 100 == 0:
            print('.', end='')
        num_reactions = 0
        while c < len(char_array)-1:
            c1 = char_array[c]
            c2 = char_array[c+1]

            if (c1.islower() and c2.isupper() and c2.lower() == c1) or \
                    (c1.isupper() and c2.islower() and c2.upper() == c1):
                if verbose:
                    print(f"Match char {c} and char {c+1}: {c1}{c2}")
                char_array.pop(c+1)
                char_array.pop(c)
                num_reactions += 1
            else:
                c += 1
        if verbose:
            print(f"Number of reactions in iteration {i}: {num_reactions}")
        if verbose:
            print(f"Remaining inputstring length: {len(char_array)}")
        i += 1
        c = 0

    if not verbose:
        print('\n')

    return char_array.tounicode()


# %% Part 1

remaining_string = react_polymer(inputstring)
print(f"Remaining polymer length after reaction is {len(remaining_string)}")

# %% Part 2

reduced_polymers = pd.DataFrame(
    index=list(string.ascii_lowercase),
    columns=[
        'input',
        'output',
    ]
)

for x in reduced_polymers.index:
    print(x, end='')
    reduced_polymers.loc[x, 'input'] = \
        inputstring.replace(x, '').replace(x.upper(), '')
    reduced_polymers.loc[x, 'output'] = \
        react_polymer(reduced_polymers.loc[x, 'input'])
print('\n')

# %%

shortest_reacted_polymer = \
    reduced_polymers.loc[:, 'output'].apply(len).sort_values().head(1)

print(
    f"The shortest reacted polymer has length "
    f"{shortest_reacted_polymer.values[0]} "
    f"and is obtained by removing all "
    f"{shortest_reacted_polymer.index[0]}-units."
)

