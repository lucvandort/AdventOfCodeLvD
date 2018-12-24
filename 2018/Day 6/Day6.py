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

coordinate_grid = \
    np.full([array_size, array_size], fill_value='', dtype='U3')


def init_coordinate_grid(row):
    coordinate_grid[row['X'], row['Y']] = row.name
    return


inputdata.apply(init_coordinate_grid, axis=1)

# %% fill grid with closest manhattan distance

x_distance_lookup = pd.DataFrame(
        index=inputdata.index,
        columns=range(array_size),
)
y_distance_lookup = pd.DataFrame(
        index=inputdata.index,
        columns=range(array_size),
)


def calculate_distance_from_coordinates(row, richting=None):
    if richting is None:
        raise Exception('Give axis!')
    coordinate = inputdata.loc[row.name, richting]
    distances = np.abs(np.arange(0-coordinate, array_size-coordinate))
    row.loc[:] = distances
    return row


x_distance_lookup = x_distance_lookup.apply(
        calculate_distance_from_coordinates,
        richting='X',
        axis=1,
)
y_distance_lookup = y_distance_lookup.apply(
        calculate_distance_from_coordinates,
        richting='Y',
        axis=1,
)


def determine_closest_manhattan_distance(x, y):
    x_distance = x_distance_lookup.loc[:, x]
    y_distance = y_distance_lookup.loc[:, y]
    manhattan_distance = x_distance + y_distance
    closest_coordinates = \
        manhattan_distance[manhattan_distance == manhattan_distance.min()]
    if len(closest_coordinates) == 1:
        return closest_coordinates.index[0].lower()
    else:
        return '.'


it = np.nditer(coordinate_grid, flags=['multi_index'], op_flags=['writeonly'])

# %% calculate closest coordinates

with it, tqdm(total=it.itersize) as pbar:
    while not it.finished:
        x, y = it.multi_index
        if it[0] == '':
            c = determine_closest_manhattan_distance(x, y)
            it[0] = c
        it.iternext()
        pbar.update()


# %% Excel dump

output = pd.DataFrame(coordinate_grid)
output.to_excel('output.xlsx')

# %% find infinite areas

infinite_areas = set()
infinite_areas |= set(np.unique(coordinate_grid[0, :]))
infinite_areas |= set(np.unique(coordinate_grid[:, 0]))
infinite_areas |= set(np.unique(coordinate_grid[-1, :]))
infinite_areas |= set(np.unique(coordinate_grid[:, -1]))

infinite_areas = set(c.upper() for c in infinite_areas)
finite_areas = \
        set(c for c in inputdata.index.values if c not in infinite_areas)

print(f"The infinite areas are: {infinite_areas}")
print(f"The finite areas are: {finite_areas}")

# %% Part 1

index, counts = np.unique(coordinate_grid, return_counts=True)
area_sizes = pd.DataFrame(index=index, columns=['count'], data=counts)
finite_area_sizes = \
        area_sizes.loc[[c.lower() for c in finite_areas], :].\
        sort_values(by='count', ascending=False) \
        + 1
largest_finite_area = finite_area_sizes.head(1)

print(
    f"The largest finite area is {largest_finite_area.index.values[0]} "
    f"and has has size {largest_finite_area.loc[:, 'count'].values[0]}"
)

# %% initialize coordinate grid 2

coordinate_grid_2 = \
    np.zeros([array_size, array_size])


def determine_total_manhattan_distance(x, y):
    x_distance = x_distance_lookup.loc[:, x]
    y_distance = y_distance_lookup.loc[:, y]
    manhattan_distance = x_distance + y_distance
    return manhattan_distance.sum()


it2 = np.nditer(
    coordinate_grid_2,
    flags=['multi_index'],
    op_flags=['writeonly']
)

# %% calculate closest coordinates

with it2, tqdm(total=it2.itersize) as pbar:
    while not it2.finished:
        x, y = it2.multi_index
        if it2[0] == 0:
            c = determine_total_manhattan_distance(x, y)
            it2[0] = c
        it2.iternext()
        pbar.update()

# %% find closest coordinates

def find_total_distance_less_than(coordinate_grid, distance=10000):
    index, counts = np.unique((coordinate_grid < distance), return_counts=True)
    closer_than = pd.DataFrame(index=index, columns=['count'], data=counts)
    return closer_than.loc[True, 'count']

# %% Part 2

print(
    f"The size of the region containing all locations which have a total "
    f"distance to all given coordinates of less than 10000 is "
    f"{find_total_distance_less_than(coordinate_grid_2)}."
)

