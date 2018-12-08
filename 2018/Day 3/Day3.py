import numpy as np
import pandas as pd

pattern = r'^#(?P<ID>[0-9]+) @ (?P<X>[0-9]+),(?P<Y>[0-9]+): ' \
    '(?P<W>[0-9]+)x(?P<H>[0-9]+)$'
columns = ['ID', 'X', 'Y', 'W', 'H']
inputdata = pd.read_csv(
    'input.txt',
    header=None,
    names=columns,
    sep=pattern,
    usecols=[1, 2, 3, 4, 5],
    index_col='ID',
    engine='python',
)

# %% Part 1

fabric_size = (
    inputdata.loc[:, ['X', 'W']].sum(axis=1).max(),
    inputdata.loc[:, ['Y', 'H']].sum(axis=1).max(),
)

fabric = np.zeros(fabric_size)

for row in inputdata.itertuples():
    fabric[row.X:row.X+row.W, row.Y:row.Y+row.H] += 1

assert fabric.sum() == (inputdata.loc[:, 'W'] * inputdata.loc[:, 'H']).sum()

overlapping_inches = (fabric > 1).sum()
print(f"The number of overlapping inches is {overlapping_inches}.")

# %% Part 2

fabric_2 = np.zeros(fabric_size)
overlapping_IDs = set()

for row in inputdata.itertuples():
    present_IDs = set(fabric_2[row.X:row.X+row.W, row.Y:row.Y+row.H].flat)
    try:
        present_IDs.remove(0.0)
    except KeyError:
        pass
    if len(present_IDs) > 0:
        present_IDs.add(row.Index)
        overlapping_IDs |= present_IDs
    fabric_2[row.X:row.X+row.W, row.Y:row.Y+row.H] = row.Index

non_overlapping_ID = set(inputdata.index) - overlapping_IDs
print(f"The only non-overlapping ID is {non_overlapping_ID}.")
