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
import math

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
    assumed to be missing. Missing point assumed to
    be equal to 'NaN.'

    If first data point is missing, the mean of the following two points
    will be imputed. If the last data point is missing, the mean of the
    previous two data points will be imputed. Otherwise, the mean of the previous
    and following point will be imputed.

    Author: River Veek
    """
    # ASSUMED THAT MISSING POINTS WILL BE == 'NaN'
    # ASSUMED THAT ONLY ONE POINT IS MISSING AT THE MOST
    # ASSUMED THAT VALUE COLUMN IS ALWAYS LAST

    # isolate last col name
    col_name = ts.columns[-1]

    # grab copy of ts (for preservation of original time series)
    ts_copy = ts

    # input will be Pandas DataFrame
    # immediately convert to list (for easier mutability)
    ts = ts.iloc[:, -1].tolist()

    for i in range(len(ts)):

        if ts[i] == "NaN":

            if i == 0:

                if len(ts) == 1:
                    ts[i] = 0  # IF ONLY VALUE == NaN, CONVERT TO 0

                elif len(ts) == 2:
                    ts[i] = ts[1]

                else:
                    mean = (ts[i + 1] + ts[i + 2]) / 2
                    ts[i] = mean

            elif i == len(ts) - 1:

                if len(ts) == 2:
                    ts[i] = ts[i - 1]

                else:
                    mean = (ts[i - 1] + ts[i - 2]) / 2
                    ts[i] = mean

            else:
                mean = (ts[i - 1] + ts[i + 1]) / 2
                ts[i] = mean

    # alter value column of ts (copy)
    ts_copy[col_name] = ts
    return ts_copy

def impute_outliers(ts):
    """
    Takes a time series and returns a time series.

    Identifies any outliers in the given time series and imputes new values
    in their place. Calculations for the new values will follow a similar
    process to impute_missing_data(); the new values will be equal to
    the mean of adjacent values.

    If first data point is an outlier, the mean of the following two points
    will be imputed. If the last data point is an outlier, the mean of the
    previous two data points will be imputed. Otherwise, the mean of the previous
    and following point will be imputed in place of the outlier.

    Multiple outliers can exist in the given time series.

    Author: River Veek
    """
    # isolate last col name
    col_name = ts.columns[-1]

    # make copy of ts for sorting purposes
    ts_copy = ts.copy()
    ts_copy = ts_copy.sort_values(by=[col_name])
    ts_copy = ts_copy.iloc[:, -1].tolist()

    # grab second copy of ts (for preservation of original time series)
    ts_original = ts

    # convert ts into list of values from last col (data)
    ts = ts.iloc[:, -1].tolist()

    # isolate Q1, Q2, IQR
    quartiles = np.quantile(ts_copy, [.25, .75], interpolation="nearest")
    iqr = quartiles[1] - quartiles[0]

    # isolate upper and lower bounds of data set (not inclusive)
    upper = quartiles[1] + 1.5 * iqr
    lower = quartiles[0] - 1.5 * iqr

    # find values that fall outside of upper or lower
    flag = 0  # equals 0 as long as outliers exist

    # run as long as outliers exist (flag == 0)
    while flag == 0:

        flag = 1

        for item in ts:

            if item > upper or item < lower:
                flag = 0  # flip flag if any outliers found (alert loop to continue)

        for i in range(len(ts)):

            if (ts[i] > upper) or (ts[i] < lower):

                if i == 0:
                    mean = (ts[i + 1] + ts[i + 2]) / 2
                    ts[i] = mean

                elif i == len(ts) - 1:
                    mean = (ts[i - 1] + ts[i - 2]) / 2
                    ts[i] = mean

                else:
                    mean = (ts[i - 1] + ts[i + 1]) / 2
                    ts[i] = mean

    ts_original[col_name] = ts
    return ts_original

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
    # WORKS WITH MULTIPLE MISSING POINTS

    # isolate last col name
    col_name = ts.columns[-1]

    # grab copy of original ts (for preservation purposes)
    ts_copy = ts

    # input will be Pandas DataFrame
    # immediately convert to list (for easier mutability)
    ts = ts.iloc[:, -1].tolist()
    new_ts = []

    longest_run = 0
    cur_run = 0
    cur_idx = 0
    start_idx = 0
    end_idx = 0

    # calculate, isolate longest run
    for i in range(len(ts)):

        if not ts[i] == "NaN":
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
        new_ts = pd.DataFrame(new_list, columns=[col_name])

    return pd.DataFrame(new_ts, columns=[col_name])
    # ts_copy[col_name] = new_ts
    # return ts_copy

def difference(ts):
    """
    Takes in an a time series and returns a time series.

    Creates a new time series with each value being the magnitude
    of the difference between each consecutive element of the provided
    time series.
    """
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
        ts_val = ts.iloc[val_id, -1]              # values should be in last column (index -1)
        next_ts_val = ts.iloc[val_id+1, -1]
        # get difference
        new_val = next_ts_val - ts_val
        # save to new dataframe
        new_ts.iloc[val_id, -1] = new_val
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
    # ASSUMES FIRST COLUMN IS TIME, SECOND COLUMN IS VALUES

    new_ts = []  # will hold values
    new_col = []  # will hold times
    flag = 0  # lets loop know when to start appending vals to new time series
    first_col = ts.iloc[:, 0].tolist()  # isolates first column
    idx = 0  # for indexing ts and first_col
    time_col_name = ts.columns[0]  # name of first col
    val_col_name = ts.columns[-1]  # name of last col

    # input will be Pandas DataFrame
    # immediately convert to list (for easier mutability)
    ts = ts.iloc[:, -1].tolist()

    if (not starting_date in first_col) or (not final_date in first_col):
        flag = 2  # lets loop know invalid arguments were entered

    for key in first_col:

        if flag == 2:
            break

        if key == starting_date:
            new_col.append(first_col[idx])
            new_ts.append(ts[idx])
            flag = 1
            idx += 1
            continue

        if flag == 1:

            if key == final_date:
                new_col.append(first_col[idx])
                new_ts.append(ts[idx])
                break

            new_col.append(first_col[idx])
            new_ts.append(ts[idx])

        idx += 1

    ret = pd.DataFrame()
    ret[time_col_name] = new_col
    ret[val_col_name] = new_ts
    return ret

def assign_time(ts, start, increment):
    """
    Assign time stamps to data points in a given time series.

    Takes a time series with no time stamps, the starting time (t_0), and
    the amount to be incremented by (delta). Assumed that start and
    increment are both integers. Returns a time series with column names
    defaulting to 'Times' and 'Values.'

    start and increment can be negative or positive values.

    Author: River Veek
    """
    # START AND INCREMENT ARE INTS
    # DEFAULT COL NAMES TO 'TIMES' AND 'VALUES'
    new_ts = []
    ts = ts.iloc[:, -1].tolist()
    times = []
    total = 0

    for i in range(len(ts)):
        times.append(start + total)
        total += increment

    ret = pd.DataFrame()
    ret["Times"] = times
    ret["Values"] = ts
    return ret

def scaling(ts):
    """
    Takes in a time series and returns a time series.

    Creates a new time series in which the magnitudes of each time series
    value is compressed into the range of [0, 1].
    """
    # make a copy
    new_ts = ts.copy()
    # convert to magnitudes
    new_ts.iloc[:, -1] = new_ts.iloc[:, -1].abs()
    # get max value
    ts_max = new_ts.iloc[:, -1].max()
    # if maximum is 0, then already scaled
    if ts_max > 0:
        # divide each value by max value to scale
        new_ts.iloc[:, -1] = new_ts.iloc[:, -1] / ts_max
    return new_ts

def standardize(ts):
    """
    Takes in a time series and returns a time series.

    Creates a new time series that translates the values of the existing
    time series to have a mean of 0 and a variance of 1.
    """
    # make a copy
    new_ts = ts.copy()
    # save mean and standard deviation for values
    val_mean = new_ts.iloc[:, -1].mean()
    val_std = new_ts.iloc[:, -1].std()
    if val_std != 0:              # to avoid division by 0 errors
        # standardize values
        new_ts.iloc[:, -1] = (new_ts.iloc[:, -1] - val_mean) / val_std
    else:
        # all values should be the mean and set to 0
        new_ts.iloc[:, -1] = new_ts.iloc[:, -1] * 0
    return new_ts

def design_matrix(ts, input_index, output_index):
    pass

def design_matrix_2(ts, mi, ti, mo, to):
    pass

def logarithm(ts):
    """
    Converts ts values to their log10 value

    possible bug: if input values from df coloumn are of type int, this may not work
    """

    nums = ts.iloc[:,-1,].to_list()


    for i in range(len(nums)):
        item = nums[i]


        if item != 0:
            item = np.log10(nums[i])
            print(item)
            ts.iloc[:,-1,][i] = item
        elif (item == 0):
            print(item)
            ts.iloc[:,-1,][i] = 0
        else:
            ts.iloc[:,-1,][i] = np.nan


    return ts



def cubic_root(ts):
    """prints warning but works"""
    nums = ts.iloc[:,-1,].to_list()

    for i in range(len(nums)):
        item = nums[i]

        if item != 0:
            item = item**(1/3)
            ts.iloc[:,-1,][i] = item
        elif (item == 0):
            ts.iloc[:,-1,][i] = 0.0
        else:
            ts.iloc[:,-1,][i] = np.nan

    return ts

def split_data(ts, perc_training, perc_valid, perc_test):
    if (perc_training + perc_valid + perc_test) != 1:
        raise Exception("Error: percentages do not add to 1")

    p = np.array([perc_training, perc_valid, perc_test])
    a = np.array(ts.iloc[:,-1,].to_list())

    length = len(a)

    sec1 = length * perc_training
    sec2 = length + perc_valid
    sec3 = length + perc_test

    print(np.split(a,(len(a)*p[:-1].cumsum()).astype(int)))






def ts2db(input_file, perc_train, perc_val, perc_test,
          input_index, output_index, output_file):
    """
    Takes in an input data file to read in the time series, as well as
    how much the user wants the data to be split into three categories:
    training, validation, and testing. Then, it creates three separate time
    series that it turns into machine learning model friendly databases with
    the input and output sizes provided, and returns those.
    """
    # read in time series data from file
    ts = fio.read_from_file(input_file)
    # split time series data into training, validation, and test sets
    ts_splits = split_data(ts, perc_train, perc_val, perc_test)
    # convert datasets into databases that can be processed by
    # a machine learning model
    train_db = design_matrix(ts_splits[0], input_index, output_index)
    val_db = design_matrix(ts_splits[1], input_index, output_index)
    test_db = design_matrix(ts_splits[2], input_index, output_index)
    # return set of databases
    return (train_db, val_db, test_db)

def db2ts(db):
    """
    Takes in a numpy matrix (database) containing a set of values and
    converts it to a time series.
    """
    # create temporary list to add time series data to
    ts_list = []
    # go through each row in database
    for row_id in range(len(db)):
        # grab each element from the first row
        if row_id == 0:                 # SUPER INEFFICIENT
            for col in db[row_id]:
                ts_list.append(col)
        # grab the last element from the remaining rows
        else:
            ts_list.append(db[row_id][-1])
    # convert to real time series data to return
    ts = pd.DataFrame(ts_list)
    return ts
