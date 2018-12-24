import pandas as pd
import numpy as np
from tqdm import tqdm

inputdata = pd.read_csv('input.txt', header=None, names=['X', 'Y'])


def index_renamer(i):
    return f'C{i}'


inputdata.rename(index=index_renamer, inplace=True)

# %% init coordinate grid

min_XY = inputdata.values.min()
max_XY = inputdata.values.max()
array_size = max_XY+min_XY+1

coordinate_grid = np.full([array_size, array_size], fill_value='', dtype='U3')


def fill_coordinate_grid(row):
    coordinate_grid[row['X'], row['Y']] = row.name
    return


inputdata.apply(fill_coordinate_grid, axis=1)

# %% fill grid


def calculate_minimum_manhattan_distance(x, y):
    x_distance = abs(inputdata.loc[:, 'X'] - x)
    y_distance = abs(inputdata.loc[:, 'Y'] - y)
    manhattan_distance = x_distance + y_distance
    closest_coordinates = \
        manhattan_distance[manhattan_distance == manhattan_distance.min()]
    if len(closest_coordinates) == 1:
        return closest_coordinates.index[0].lower()
    else:
        return '.'


it = np.nditer(coordinate_grid, flags=['multi_index'], op_flags=['writeonly'])


# %%

with it, tqdm(total=it.itersize) as pbar:
    while not it.finished:
        x, y = it.multi_index
        if it[0] == '':
            c = calculate_minimum_manhattan_distance(x, y)
            it[0] = c
        it.iternext()
        pbar.update()


# %% Excel dump

output = pd.DataFrame(coordinate_grid)
output.to_excel('output.xlsx')
