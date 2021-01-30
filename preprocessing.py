"""
Preprocessing Functions
"""

########################
# IMPORTS AND GLOBALS
########################

import pandas as pd
import file_io as fio
import matplotlib.pyplot as plt
import numpy as np


######################
# HELPER FUNCTIONS
######################


#########################
# PREPROCESSING FUNCTIONS
#########################

def denoise(ts):
    """
    Takes time series and returns a new time series
    Thought this was my responsibility, call this a draft -Nick Titzler
    """
    frame = pd.Series(ts.series).to_frame()

    print(frame)

    rolling_mean = frame.rolling(window=10).mean()

    
    return rolling_mean

def impute_missing_data(ts):
    """
    Takes a time series and returns a new time series.

    Computes missing data point by taking mean of
    adjacent points in time. Only one data point is
    assumed to be missing.

    If first data point is missing, the mean of the following two points
    will be imputed. If the last data point is missing, the mean of the
    previous two data points will be imputed.

    Author: River Veek
    """
    new_ts = TimeSeries()

    for i in range(len(ts)):

        # ASSUMED THAT MISSING POINTS WILL BE == NONE
        if not ts[i] == None:
            new_ts.append(ts[i])

        else:
            # ASSUMED THAT ONLY ONE POINT IS MISSING
            if i == 0:  # if first point missing, take mean of next two
                mean = (ts[i + 1] + ts[i + 2]) / 2

            elif i == len(ts) - 1:  # if last point missing, take mean of previous two
                mean = (ts[i - 1] + ts[i - 2]) / 2

            else:  # else, take mean of previous and next point
                mean = (ts[i - 1] + ts[i + 1]) / 2

            new_ts.append(mean)

    return new_ts

def impute_outliers(ts):
    pass

def longest_continuous_run(ts):
    """
    Takes a time series and returns a time series.

    Computes the longest continuous run and returns that
    subset run as a new time series. Here, the longest continuous run
    is the longest continuous time series subset without any empty/None
    values.

    This function allows for time series inputs with one or more (>= 1)
    missing data points.

    Author: River Veek
    """
    new_ts = TimeSeries()
    longest_run = 0
    cur_run = 0
    cur_idx = 0
    start_idx = 0
    end_idx = 0

    # WORKS WITH MULTIPLE MISSING POINTS

    # calculate, isolate longest run
    for i in range(len(ts)):

        if not ts[i] == None:
            cur_run += 1
        else:
            cur_run = 0

        if cur_run > longest_run:
            longest_run = cur_run
            end_idx = cur_idx
            start_idx = cur_idx - cur_run + 1

        cur_idx += 1

    # add data points in longest run to new time series
    for i in range(start_idx, end_idx + 1):
        new_ts.append(ts[i])

    # if time series has no valid points, return empty time series
    if start_idx == end_idx:
        new_ts = TimeSeries()

    return new_ts

def difference(ts):
    """
    Takes in an a time series and returns a time series.

    Creates a new time series with each value being the magnitude
    of the difference between each consecutive element of the provided
    time series.
    """
    # ensure data is properly formatted
    if len(ts.keys()) != 2:
        print("Error: Improperly formatted data")
        return
    # ensure enough data entries
    if len(ts) < 2:
        print("Error: Not enough data")
        return
    # make a copy
    new_ts = ts.copy()
    # save index to last entry
    last_entry = len(ts) - 1
    for val_id in range(last_entry):
        # grab two consecutive values
        ts_val = ts.iloc[val_id, 1]              # values should be in second column (index 1)
        next_ts_val = ts.iloc[val_id+1, 1]
        # get difference
        new_val = next_ts_val - ts_val
        # save to new dataframe
        new_ts.iloc[val_id, 1] = new_val
    # remove last (unaltered) value
    new_ts.drop(index=last_entry)
    return new_ts

def clip(ts, starting_date, final_date):
    """
    Takes a time series, the starting date to clip the time series
    by, and the ending date to clip the time series by. No assumption
    is made about the types of starting_date and final_date; these two
    parameters will only be assumed to be valid keys of the time series ts.

    If starting_date greater than (>) final_date, then time series ts is
    clipped from starting_date to the end of ts.

    If starting_date or final_date are invalid (not valid keys of ts),
    an empty time series will be returned.

    Returns a new, clipped time series (does not alter original).

    Author: River Veek
    """
    new_ts = TimeSeries()
    flag = 0  # lets loop know when to start appending vals to new time series

    if (not starting_date in ts) or (not final_date in ts):
        flag = 2  # lets loop know invalid arguments were entered

    for key in ts:

        if flag == 2:
            break

        if key == starting_date:
            new_ts[key] = ts[key]
            flag = 1

        if flag == 1:

            if key == final_date:
                new_ts[key] = ts[key]
                break

            new_ts[key] = ts[key]

    return new_ts

def assign_time(ts, start, increment):
    """
    Assign time stamps to data points in a given time series.

    Takes a time series with no time stamps, the starting time (t_0), and
    the amount to be incremented by (delta). Assumed that start and
    increment are both integers.

    start and increment can be negative or positive values.

    Author: River Veek
    """
    # ASSUMED THAT TS IS A LIST, START AND INCREMENT ARE INTS
    new_ts = TimeSeries()
    total = 0

    for item in ts:
        new_ts[str(start + total)] = item
        total += increment

    return new_ts

def scaling(ts):
    """
    Takes in a time series and returns a time series.

    Creates a new time series in which the magnitudes of each time series
    value is compressed into the range of [0, 1].
    """
    # ensure data is properly formatted
    if len(ts.keys()) != 2:
        print("Error: Improperly formatted data.")
        return
    # make a copy
    new_ts = ts.copy()
    # convert to magnitudes
    new_ts.iloc[:, 1] = new_ts.iloc[:, 1].abs()
    # get max value
    ts_max = ts.iloc[:, 1].max()
    # if maximum is 0, then already scaled
    if ts_max > 0:
        # divide each value by max value to scale
        new_ts.iloc[:, 1] = new_ts.iloc[:, 1] / ts_max
    return new_ts

def standardize(ts):
    """
    Takes in a time series and returns a time series.

    Creates a new time series that translates the values of the existing
    time series to have a mean of 0 and a variance of 1.
    """
    # ensure data is properly formatted
    if len(ts.keys()) != 2:
        print("Error: Improperly formatted data.")
        return
    # make a copy
    new_ts = ts.copy()
    # save mean and standard deviation for values
    val_mean = new_ts.iloc[:, 1].mean()
    val_std = new_ts.iloc[:, 1].std()
    try:
        # standardize values
        new_ts.iloc[:, 1] = (new_ts.iloc[:, 1] - val_mean) / val_std
    # in case val_std == 0
    except ZeroDivisionError:
        print("Error: Cannot standardize. No deviation.")
        return
    return new_ts

def design_matrix(ts, input_index, output_index):
    pass

def design_matrix_2(ts, mi, ti, mo, to):
    pass

def logarithm(ts):
	"""
	nickt
	"""
	frame = pd.Series(ts.series).to_frame()
	frame['norm'] = (1+frame[0])/2
	frame['lognorm'] = np.log(frame['norm'])

def cubic_root(ts):
	"""
	nickt
	"""
	pass

def split_data(ts, perc_training, perc_valid, perc_test):
	"""
	nickt
	"""
	pass

def ts2db(input_file, perc_train, perc_val, perc_test,
          input_index, output_index, output_file):
    pass
