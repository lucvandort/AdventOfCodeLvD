import string
import pandas as pd
from math import factorial
from difflib import ndiff
from itertools import combinations


identifier_input = pd.read_csv('input.txt', header=None)

#%% Part 1


def count_letters(identifier):
    letter_count = {}
    for letter in string.ascii_lowercase:
        letter_count[letter] = identifier.count(letter)
    return letter_count


identifiers_with_double_letters = []
identifiers_with_triple_letters = []


for identifier in identifier_input.loc[:, 0]:
    letter_count = count_letters(identifier)
    if 2 in letter_count.values():
        identifiers_with_double_letters.append(identifier)
    if 3 in letter_count.values():
        identifiers_with_triple_letters.append(identifier)

checksum = len(identifiers_with_double_letters) * \
    len(identifiers_with_triple_letters)

#%% Part 2

diff_columns = [
    'id1',
    'id2',
    'ndiff',
    'num_changes',
]

n = len(identifier_input)
r = 2
num_comparisons = int(factorial(n) / (factorial(r) * factorial(n-r)))

identifier_comparison = pd.DataFrame(
    index=range(num_comparisons),
    columns=diff_columns,
)

identifier_comparison.loc[:, ['id1', 'id2']] = \
    list(combinations(identifier_input.loc[:, 0], r))


def compare_ids(row):
    id_diff = list(ndiff(row['id1'], row['id2']))
    row['ndiff'] = id_diff
    row['num_changes'] = ''.join(id_diff).count('+')
    return row


identifier_comparison.apply(compare_ids, axis=1, )

best_match = identifier_comparison[
    identifier_comparison.loc[:, 'num_changes'] == 1]
match_ndiff = best_match.loc[:, 'ndiff'].values[0]
final_id = ''.join(
    [c for c in match_ndiff if '+' not in c and '-' not in c]
    ).replace(' ', '')
