import pandas as pd
import numpy as np
from tqdm import tqdm

with open('input.txt') as inputfile:
    inputdata = pd.Series(
        inputfile.read().strip().split(),
        name='data',
        dtype=int
    )

columns = [
    'parent',
    'num_children',
    'children',
    'num_metadata',
    'metadata',
]
nodes = pd.DataFrame(columns=columns, dtype='object')

# %% Part 1


def process_node(inputdata, i=0, parent=None, pbar=None):
    node_index = len(nodes)
    num_children = inputdata[i]
    num_metadata = inputdata[i+1]
    nodes.loc[node_index, 'num_children'] = num_children
    nodes.loc[node_index, 'children'] = []
    nodes.loc[node_index, 'num_metadata'] = num_metadata
    nodes.loc[node_index, 'metadata'] = []
    try:
        nodes.loc[node_index, 'parent'] = parent.name
    except AttributeError:
        nodes.loc[node_index, 'parent'] = None

    current_node = nodes.loc[node_index, :]
    i += 2
    if pbar is not None:
        pbar.update(2)

    for child in range(num_children):
        childnode, i = process_node(
            inputdata,
            i=i,
            parent=current_node,
            pbar=pbar
        )
        current_node.loc['children'] += [childnode.name]

    current_node.loc['metadata'] += \
        list(inputdata[list(range(i, i+num_metadata))])
    i += num_metadata
    if pbar is not None:
        pbar.update(num_metadata)

    return current_node, i


with tqdm(total=len(inputdata)) as pbar:
    process_node(inputdata, pbar=pbar)

sum_of_metadata = np.asarray(nodes.loc[:, 'metadata'].sum()).sum()
print(f"The sum of all node metadata is {sum_of_metadata}.")

# %% Part 2


def calculate_root_value(nodes, node_index=0, pbar=None):
    current_node = nodes.loc[node_index, :]
    node_value = 0

    if current_node.loc['num_children'] == 0:
        node_value = np.asarray(current_node.loc['metadata']).sum()

    else:
        for metadata in current_node.loc['metadata']:
            try:
                node_value += calculate_root_value(
                    nodes,
                    node_index=current_node.loc['children'][metadata-1],
                    pbar=pbar,
                )
            except IndexError:
                continue

    pbar.update()
    return node_value


with tqdm() as pbar:
    root_value = calculate_root_value(nodes, pbar=pbar)

print(f"The root node value is {root_value}.")
