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


# %%

record_columns = [
    'month',
    'day',
    'guard',
]
record_columns.extend(range(60))

dates = list(processed_data.groupby(['month', 'day']).groups)

records = pd.DataFrame(
    data=0,
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
            ] = 1
    elif row.event == 'wakes up':
        records.loc[
            (records.month == row.month) & (records.day == row.day),
            np.arange(row.minute, 60)
            ] = 0

# %% Part 1
guards = list(processed_data.groupby('guard').groups)
columns = [
    'sleep_minutes',
    'most_sleepy_minute',
    'sleep_during_most_sleepy_minute',
]
guard_sleep_stats = pd.DataFrame(index=guards, columns=columns)
guard_sleep_stats.loc[:, 'sleep_minutes'] = 0

for record in records.itertuples():
    guard_sleep_stats.loc[record.guard, 'sleep_minutes'] += record.count(1)

for guard in guards:
    most_sleep_stat = records.loc[
        (records.loc[:, 'guard'] == guard), np.arange(0, 60)
        ].sum().sort_values(ascending=False).head(1)
    guard_sleep_stats.loc[guard, 'most_sleepy_minute'] = \
        most_sleep_stat.index
    guard_sleep_stats.loc[guard, 'sleep_during_most_sleepy_minute'] = \
        most_sleep_stat.values

most_sleepy_guard = guard_sleep_stats.sort_values(
    by='sleep_minutes', ascending=False).head(1).index.values
most_sleepy_minute = guard_sleep_stats.loc[
    most_sleepy_guard, 'most_sleepy_minute'].values
guard_id_sleepy_minute_multiplier = int(most_sleepy_guard) * most_sleepy_minute

print(
    f"The the ID of the most sleepy guard ({most_sleepy_guard}) "
    "multiplied by his most "
    f"sleepy minute ({most_sleepy_minute}) is "
    f"{guard_id_sleepy_minute_multiplier}"
)

# %% Part 2

most_consequent_sleeping_guard = guard_sleep_stats.sort_values(
    by='sleep_during_most_sleepy_minute', ascending=False).head(1).index.values
most_sleepy_minute_2 = guard_sleep_stats.loc[
    most_consequent_sleeping_guard, 'most_sleepy_minute'].values
guard_id_sleepy_minute_multiplier_2 = int(most_consequent_sleeping_guard) * \
    most_sleepy_minute_2

print(
    f"The the ID of the most consequent sleeping guard "
    f"({most_consequent_sleeping_guard}) multiplied by his most "
    f"sleepy minute ({most_sleepy_minute}) is "
    f"{guard_id_sleepy_minute_multiplier_2}"
)