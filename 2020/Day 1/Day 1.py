#%% imports
import pandas as pd
import numpy as np

#%%
data = pd.read_csv('input.txt', header=None)

num_items = len(data)

data = data.values.reshape(num_items)



#%% deel 1, methode 1, werkt niet :(
for i in range(num_items):
    for j in range(i, num_items):
        som = data[i] + data[j]
        print(i, data[i], j, data[j], som)
        if som == 2020:
            break

product = data[i] * data[j]

print(f"Regel {i} is {data[i]}")
print(f"Regel {j} is {data[j]}")
print(f"De som is {som}")
print(f"Het product is {product}")


# %% deel 1, methode 2, werkt wel :)

som = np.zeros((num_items, num_items))

for i in range(num_items):
    som[:, i] = data + data[i]

check_2020 = np.where(som == 2020)
n1, n2= check_2020[0]

som = data[n1] + data[n2]
product = data[n1] * data[n2]

print(f"Regel {n1} is {data[n1]}")
print(f"Regel {n2} is {data[n2]}")
print(f"De som is {som}")
print(f"Het product is {product}")

# %% deel 2

som3d = np.zeros((num_items, num_items, num_items))

for i in range(num_items):
    for j in range(num_items):
        som3d[:, i, j] = data + data[i] + data[j]


check_2020_3d = np.where(som3d == 2020)
n1, n2, n3 = np.unique(check_2020_3d[0])

som = data[n1] + data[n2] + data[n3]
product = data[n1] * data[n2] * data[n3]

print(f"Regel {n1} is {data[n1]}")
print(f"Regel {n2} is {data[n2]}")
print(f"Regel {n3} is {data[n3]}")
print(f"De som is {som}")
print(f"Het product is {product}")

# %%
