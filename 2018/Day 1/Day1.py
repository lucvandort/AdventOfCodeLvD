import pandas as pd

frequency_changes = pd.read_csv('input.txt', header=None)

sum_of_frequency_changes = frequency_changes.sum(0)
