import pandas as pd

regex = r'^.* ([A-Z]) .* ([A-Z]) .*[.]$'
inputdata = pd.read_csv(
    'input.txt',
    header=None,
    names=['step', 'before'],
    sep=regex,
    usecols=[1, 2, ],
    engine='python',
)

# %%

# find all steps
all_steps = set(inputdata.values.reshape(inputdata.size))

# find prerequisites for each step
prerequisites = {
    S: set(inputdata[inputdata.loc[:, 'before'] == S].loc[:, 'step'])
    for S in all_steps
}

# find following steps for each step
followers = {
    S: set(inputdata[inputdata.loc[:, 'step'] == S].loc[:, 'before'])
    for S in all_steps
}

# %% Part 1

output = ''
remaining_prerequisites = \
    {step: preqs.copy() for step, preqs in prerequisites.items()}

while len(output) < len(all_steps):
    prepared_steps = []
    for step, step_prerequisites in remaining_prerequisites.items():
        if len(step_prerequisites) == 0:
            prepared_steps += [step]
    print(prepared_steps)
    prepared_steps.sort(reverse=True)
    next_step = prepared_steps.pop()
    output += next_step
    del remaining_prerequisites[next_step]
    for step, step_prerequisites in remaining_prerequisites.items():
        try:
            step_prerequisites.remove(next_step)
        except KeyError:
            pass

print(
    f"The order in which the steps should be executed is {output}."
)
