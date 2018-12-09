import pandas as pd
import numpy as np
import re

pattern = r"^\[1518-([0-9]{2})-([0-9]{2}) ([0-9]{2}):([0-9]{2})\] (.*)$"
columns = [
    'month',
    'day',
    'hour',
    'minute',
    'event',
]
inputdata = pd.read_csv(
    'input.txt',
    header=None,
    sep=pattern,
    names=columns,
    usecols=[1, 2, 3, 4, 5, ],
    engine='python',
)
inputdata.sort_values(by=['month', 'day', 'hour', 'minute', ], inplace=True)

columns = [
    'month',
    'day',
    'hour',
    'minute',
    'guard',
    'event',
]
processed_data = pd.DataFrame(index=inputdata.index, columns=columns)
processed_data.loc[:, ['month', 'day', 'hour', 'minute', 'event']] = \
    inputdata.loc[:, ['month', 'day', 'hour', 'minute', 'event']]


def transform_dates(row):
    if row.hour == 23:
        row.day += 1
        row.hour = 0
        row.minute -= 60
    if row.month in [1, 3, 5, 7, 8, 10, 12, ] and row.day == 32:
        row.month += 1
        row.month %= 12
        row.day = 1
    elif row.month in [4, 6, 9, 11, ] and row.day == 31:
        row.month += 1
        row.day = 1
    elif row.month == 2 and row.day == 29:
        row.month += 1
        row.day = 1
    return row


processed_data.apply(transform_dates, axis=1)

current_guard_id = None


def process_guard_actions(row):
    global current_guard_id
    if row.event[0] == 'G':
        current_guard_id = re.sub('[^0-9]', '', row.event)
        row.event = 'begins shift'
    row.guard = current_guard_id
    return row


processed_data.apply(process_guard_actions, axis=1)


# %% Part 1

record_columns = [
    'month',
    'day',
    'guard',
]
record_columns.extend(range(60))

dates = list(processed_data.groupby(['month', 'day']).groups)

records = pd.DataFrame(
    data='.',
    index=range(len(dates)),
    columns=record_columns,
)
records.loc[:, ['month', 'day', ]] = np.asarray(dates)

current_date = (None, None)
current_guard = None

# %%
for row in processed_data.itertuples():
    if row.event == 'begins shift':
        records.loc[
            (records.month == row.month) & (records.day == row.day),
            'guard'
            ] = row.guard
    elif row.event == 'falls asleep':
        records.loc[
            (records.month == row.month) & (records.day == row.day),
            np.arange(row.minute, 60)
            ] = '#'
    elif row.event == 'wakes up':
        records.loc[
            (records.month == row.month) & (records.day == row.day),
            np.arange(row.minute, 60)
            ] = '.'

# %%
guards = list(processed_data.groupby('guard').groups)
columns = [
    'sleep_minutes',
]
guard_sleep_stats = pd.DataFrame(index=guards, columns=columns)
guard_sleep_stats.loc[:, 'sleep_minutes'] = 0

for record in records.itertuples():
    guard_sleep_stats.loc[record.guard, 'sleep_minutes'] += record.count('#')

most_sleepy_guard = guard_sleep_stats.sort_values(
    by='sleep_minutes', ascending=False).head(1).index
