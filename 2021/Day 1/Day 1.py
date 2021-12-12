import pandas as pd

data = pd.read_csv('input.txt', names=['data'])

# %% part 1

verschil = data.iloc[1:].values - data.iloc[:-1].values

toename = (verschil > 0).sum()

# %% part 2

data2 = data.iloc[:-2].values + data.iloc[1:-1].values + data.iloc[2:].values

verschil2 = data2[1:] - data2[:-1]

toename2 = (verschil2 > 0).sum()
