import pandas as pd
import string

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


def determine_next_step(remaining_prerequisites):
    prepared_steps = []
    for step, step_prerequisites in remaining_prerequisites.items():
        if len(step_prerequisites) == 0:
            prepared_steps += [step]
    prepared_steps.sort(reverse=True)
#    print(prepared_steps)
    try:
        next_step = prepared_steps.pop()
    except IndexError:
        next_step = None
    return next_step


def finish_step(remaining_prerequisites, step, followers):
    for step_follower in followers[step]:
        remaining_prerequisites[step_follower].remove(step)
    return


output = ''
remaining_prerequisites = \
    {step: preqs.copy() for step, preqs in prerequisites.items()}

while len(output) < len(all_steps):
    next_step = determine_next_step(remaining_prerequisites)
    output += next_step
    del remaining_prerequisites[next_step]
    finish_step(remaining_prerequisites, next_step, followers)

print(
    f"The order in which the steps should be executed is {output}."
)

# %% Part 2

# define processing time for each step
processing_time = dict(zip(list(string.ascii_uppercase), range(61, 61+26)))
num_workers = 5

output2 = ''
remaining_prerequisites = \
    {step: preqs.copy() for step, preqs in prerequisites.items()}
event_tracker = pd.DataFrame(
    index=range(2*26+1),
    columns=['time', 'begin', 'end', 'active_workers']
)
current_event = 0
active_workers = 0
active_tasks = set()
current_time = 0

event_tracker.loc[current_event, :] = (
    current_time,
    '',
    '',
    active_workers
)
current_event += 1

while len(output2) < len(all_steps):
    next_step = determine_next_step(remaining_prerequisites)

    if active_workers < num_workers and next_step is not None:
        active_workers += 1
        event_tracker.loc[current_event, :] = (
            current_time,
            next_step,
            '',
            active_workers,
        )
        current_event += 1
        print(f"Start task {next_step} at T={current_time}")
        event_tracker.loc[current_event, :] = (
            current_time + processing_time[next_step],
            '',
            next_step,
            '',
        )
        current_event += 1
        del remaining_prerequisites[next_step]

    elif active_workers == num_workers or next_step is None:
        finishing_task = event_tracker[
            event_tracker.loc[:, 'time'] > current_time
            ].sort_index().sort_values(by=['time']).head(1)
        current_time = finishing_task.loc[:, 'time'].values[0]
        active_workers -= 1
        event_tracker.loc[finishing_task.index, 'active_workers'] = \
            active_workers
        finishing_step = finishing_task.loc[:, 'end'].values[0]
        output2 += finishing_step
        print(f"Finishing task {finishing_step} at T={current_time}")
        finish_step(remaining_prerequisites, finishing_step, followers)

total_time = event_tracker.loc[:, 'time'].max()

print(
    f"The timed order in which the steps are executed is {output2}."
)
print(
    f"The total time it takes to complete the steps is {total_time}."
)
