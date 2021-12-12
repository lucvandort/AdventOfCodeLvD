import pandas as pd

data = pd.read_csv('input.txt', names=['direction', 'amount'], sep=' ', )

# %% part 1

up = data.loc[:, 'direction'] == 'up'
down = data.loc[:, 'direction'] == 'down'
forward = data.loc[:, 'direction'] == 'forward'

horizontal = data.loc[forward, 'amount'].sum()
depth = data.loc[down, 'amount'].sum() - data.loc[up, 'amount'].sum()

answer = horizontal * depth

# %% part 2

data.loc[0, 'aim'] = 0

for row in range(1, len(data)):
    direction = data.loc[row, 'direction']
    if direction == 'up':
        data.loc[row, 'aim'] = data.loc[row-1, 'aim'] - data.loc[row, 'amount']
    elif direction == 'down':
        data.loc[row, 'aim'] = data.loc[row-1, 'aim'] + data.loc[row, 'amount']
    else:
        data.loc[row, 'aim'] = data.loc[row-1, 'aim']

depth2 = (data.loc[forward, 'amount'] * data.loc[forward, 'aim']).sum()

answer2 = horizontal * depth2
