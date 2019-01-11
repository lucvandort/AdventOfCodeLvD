import numpy as np
from tqdm import tqdm


# %%


class FuelCellGrid():

    def __init__(self, grid_serial_number, grid_size=(300, 300)):

        self.grid_size = grid_size
        self.grid_serial_number = grid_serial_number

        self.grid = np.zeros(self.grid_size, dtype=int)

        # Find the fuel cell's rack ID, which is its X coordinate plus 10.
        for i in range(self.grid_size[0]):
            self.grid[:, i] = i + 10

        # Begin with a power level of the rack ID times the Y coordinate.
        for i in range(self.grid_size[1]):
            self.grid[i, :] *= i

        # Increase the power level by the value of the grid serial number
        # (your puzzle input).
        self.grid += self.grid_serial_number

        # Set the power level to itself multiplied by the rack ID.
        for i in range(self.grid_size[0]):
            self.grid[:, i] *= i + 10

        # Keep only the hundreds digit of the power level
        # (so 12345 becomes 3; numbers with no hundreds digit become 0).
        self.grid //= 100
        self.grid %= 10

        # Subtract 5 from the power level.

        self.grid -= 5

    def find_largest_total_power_area(self, size=3):
        len_x, len_y = self.grid_size
        summation_grid = np.zeros((len_y-(size-1), len_x-(size-1)))

        array_shift_indices = [
            (sh_y, sh_x)
            for sh_x in range(size)
            for sh_y in range(size)
        ]

        for sh_y, sh_x in array_shift_indices:
            summation_grid += self.grid[
                sh_y:len_y-(size-1)+sh_y,
                sh_x:len_x-(size-1)+sh_x
            ]

        max_y, max_x = np.unravel_index(
            np.argmax(summation_grid),
            summation_grid.shape
        )
        total_power = np.amax(summation_grid)

        return max_x, max_y, size, total_power

    def optimize_largest_total_power_area_size(self):
        best_result = (0, 0, 0, 0)
        with tqdm(total=min(self.grid_size)) as pb:
            for size in range(1, min(self.grid_size)+1):
                result = self.find_largest_total_power_area(size)
                if result[3] > best_result[3]:
                    best_result = result
                pb.update()
        return best_result

# %% Tests

grid_57 = FuelCellGrid(57)
assert grid_57.grid[79, 122] == -5

grid_39 = FuelCellGrid(39)
assert grid_39.grid[196, 217] == 0

grid_71 = FuelCellGrid(71)
assert grid_71.grid[153, 101] == 4

# %% More Tests

grid_18 = FuelCellGrid(18)
assert grid_18.find_largest_total_power_area() == (33, 45, 3, 29)

grid_42 = FuelCellGrid(42)
assert grid_42.find_largest_total_power_area() == (21, 61, 3, 30)

# %% Part 1

input_grid_size = (300, 300)
input_grid_serial_number = 7689

part1_grid = FuelCellGrid(input_grid_serial_number, input_grid_size)
max_power = part1_grid.find_largest_total_power_area()

print(
    f"The maximum power of {max_power[3]} is found at "
    f"({max_power[0]},{max_power[1]})."
)

# %% Part 2

best_max_power = part1_grid.optimize_largest_total_power_area_size()

print(
    f"The maximum power of {best_max_power[3]} is found at "
    f"({best_max_power[0]},{best_max_power[1]})"
    f"for fuel cell square size {best_max_power[2]}."
)
