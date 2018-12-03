import pandas as pd
import numpy as np
from numba import jit

frequency_changes = pd.read_csv('input.txt', header=None)

#%% Part 1

sum_of_frequency_changes = frequency_changes.sum(0)

#%% Part 2

frequency_changes_array = np.array(frequency_changes.loc[:, 0])


@jit(nopython=True)
def double_frequency_checker(frequency_changes_array, current_frequency=0):
    frequency_counter = [current_frequency]
    iteration_counter = 0

    while(True):
        iteration_counter = iteration_counter + 1
        print("Iteration", iteration_counter)
        for df in frequency_changes_array:
            current_frequency = current_frequency + df
            if current_frequency in frequency_counter:
                print("First double frequency at", current_frequency, "Hz")
                return current_frequency
            else:
                frequency_counter.append(current_frequency)


first_double_frequency = double_frequency_checker(frequency_changes_array)
