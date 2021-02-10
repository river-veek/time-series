"""
----------------------------------------------------------------------------------------
Preprocessing Functions

Authors - River Veek, Nick Titzler, Cameron Jordal
Group - Keyboard Warriors
Last Modified - 2/9/2021
----------------------------------------------------------------------------------------
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

pd.options.mode.chained_assignment = None


#########################
# PREPROCESSING FUNCTIONS
#########################

def denoise(ts, increment=10):
    """
    Takes time series dataframe and a increment value and returns a new time series

    Denoises data by applying a rolling mean whose size is determinded by the
    increment parameter. The function will not allow an increment that is too small,
    as denoising the data would result in the data being reduced to greatly. The function will 
    exit if this possibility occurs.

    Calls: NA
    CALLED BY: TS_Tree.execute_tree()

    Author: Nick Titzler
    """

    increment = int(increment)

    if increment >= (len(ts.iloc[:,-1])):
        print("ERROR: by using increment size ",increment," your data will be converted to NaN")
        print("Now exiting")
        exit()
    # function that denoises data
    ts.iloc[:,-1] = ts.iloc[:,-1].rolling(increment).mean()

    # function that removes NaN values
    ts = ts.dropna()

    return ts


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

    # isolate last column of time series
    col_name = ts.columns[-1]

    # grab copy of ts (for preservation of original time series)
    ts_copy = ts

    # input will be Pandas DataFrame
    # immediately convert to list (for easier mutability)
    ts = ts.iloc[:, -1].tolist()

    # loop through each value in ts and check if 'NaN'
    for i in range(len(ts)):

        # look for 'NaN' values
        if np.isnan(ts[i]):

            # if first value is 'NaN'
            if i == 0:

                # if 'NaN' is only value, convert to 0
                if len(ts) == 1:
                    ts[i] = 0

                # if only two values exist, convert to second value
                elif len(ts) == 2:
                    ts[i] = ts[1]

                # else, convert to mean of following two values
                else:
                    mean = (ts[i + 1] + ts[i + 2]) / 2
                    ts[i] = mean

            # if last value is 'NaN'
            elif i == len(ts) - 1:

                # if only two values exist, convert to first value
                if len(ts) == 2:
                    ts[i] = ts[i - 1]

                # else, convert to mean of previous two values
                else:
                    mean = (ts[i - 1] + ts[i - 2]) / 2
                    ts[i] = mean

            # else, convert to mean of previous and following value
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
    # isolate last column of time series
    col_name = ts.columns[-1]

    # make copy of ts for sorting purposes
    ts_copy = ts.copy()
    ts_copy = ts_copy.sort_values(by=[col_name])
    ts_copy = ts_copy.iloc[:, -1].tolist()

    # grab second copy of ts (for preservation of original time series)
    ts_original = ts

    # convert ts into list of values from last (data) column
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

        flag = 1  # temporarily flip flag

        # examine each value in ts
        for item in ts:

            if item > upper or item < lower:
                flag = 0  # flip flag back if any outliers found (alert loop to continue)

        # examine each value in ts AND convert it to non-outlier
        for i in range(len(ts)):

            if (ts[i] > upper) or (ts[i] < lower):

                # if first value is outlier, convert to mean of following two values
                if i == 0:
                    mean = (ts[i + 1] + ts[i + 2]) / 2
                    ts[i] = mean

                # if last value is outlier, convert to mean of previous two values
                elif i == len(ts) - 1:
                    mean = (ts[i - 1] + ts[i - 2]) / 2
                    ts[i] = mean

                # else, convert to mean of previous and following value
                else:
                    mean = (ts[i - 1] + ts[i + 1]) / 2
                    ts[i] = mean

    # reassign original values column
    ts_original[col_name] = ts
    return ts_original

def longest_continuous_run(ts):
    """
    Takes a time series and returns a time series.

    Computes the longest continuous run and returns that
    subset run as a new time series. Here, the longest continuous run
    is the longest continuous time series subset without any "NaN" values.

    This function allows for time series inputs with one or more (>= 1)
    missing data points.

    If all values are "NaN," an empty DataFrame will be returned.

    Author: River Veek
    """
    # WORKS WITH MULTIPLE MISSING POINTS

    # create dictionary of all columns with empty value lists
    # will return d as DataFrame
    d = {}
    for col in ts:
        d[col] = []

    # grab copy of d (for preserverion purposes)
    # will create and return a DataFrame of this if start_idx and end_idx are equal
    d_copy = {}
    for col in ts:
        d_copy[col] = []

    # grab copy of original ts (for preservation purposes)
    ts_copy = ts

    # input will be Pandas DataFrame
    # immediately convert to list (for easier mutability)
    ts = ts.iloc[:, -1].tolist()

    longest_run = 0  # will hold length of longest run
    cur_run = 0  # will hold length of current longest run
    cur_idx = 0  # current index in ts
    start_idx = 0  # starting index of ts
    end_idx = 0  # ending index of ts

    # calculate, isolate longest run
    for i in range(len(ts)):

        if not np.isnan(ts[i]):
            cur_run += 1

        else:
            cur_run = 0

        # if new longest run is found, reinitialize longest run
        if cur_run > longest_run:
            longest_run = cur_run
            end_idx = cur_idx
            start_idx = cur_idx - cur_run + 1

        cur_idx += 1

    # add all data from longest run to main dictionary (d)
    for i in range(start_idx, end_idx + 1):
        for col in d:
            d[col].append(ts_copy[col][i])

    # if time series has no valid points, return empty time series (d_copy)
    if start_idx == end_idx:
        return pd.DataFrame(d_copy)

    return pd.DataFrame(d)

def difference(ts):
    """
    Takes in an a time series and returns a time series.

    Creates a new time series with each value being the magnitude
    of the difference between each consecutive element of the provided
    time series.
    """
    # empty return when not enough to calculate difference
    if len(ts) < 2:
        new_ts = pd.DataFrame(columns=ts.keys())
        return new_ts
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
        # save magnitude to new dataframe
        new_ts.iloc[val_id, -1] = abs(new_val)
    # remove last (unaltered) value
    new_ts = new_ts.drop(index=last_entry)
    return new_ts

def clip(ts, starting_date, final_date):
    """
    Takes a time series, the starting date to clip the time series
    by, and the ending date to clip the time series by and returns
    a modified time series. starting_date and final_date must be of
    type float; these two parameters will be assumed to be valid items
    of the time series ts.

    If starting_date greater than (>) final_date, then time series ts is
    clipped from starting_date to the end of ts.

    If starting_date or final_date are invalid (not valid keys of ts),
    an empty time series will be returned.

    Returns a new, clipped time series (does not alter original).

    Author: River Veek
    """
    # ASSUMES FIRST COLUMN IS TIME, LAST COLUMN IS VALUES

    # grab copy of ts (for preservation purposes)
    ts_copy = ts

    # make blank dictionary to add future column vals to
    d = {}
    for col in ts_copy:
        d[col] = []

    new_ts = []  # will hold values
    new_col = []  # will hold times
    flag = 0  # lets loop know when to start appending vals to new time series
    first_col = ts.iloc[:, 0].tolist()  # isolates first column
    idx = 0  # for indexing ts and first_col
    time_col_name = ts.columns[0]  # name of first col
    val_col_name = ts.columns[-1]  # name of last col

    # input will be DataFrame
    # immediately convert to list (for easier mutability)
    ts = ts.iloc[:, -1].tolist()

    # find section in ts to clip
    for key in first_col:

        if key == starting_date:

            # if starting and ending dates are the same, add only that information to d and break
            if starting_date == final_date:
                for col in d:

                    d[col].append(ts_copy[col][idx])

                break

            # else, begin to add information to d in sequence
            for col in d:

                d[col].append(ts_copy[col][idx])

            flag = 1
            idx += 1
            continue

        # if starting date has been found, begin adding information to d
        if flag == 1:

            # if final date is found, add remaining information and break
            if key == final_date:
                for col in d:

                    d[col].append(ts_copy[col][idx])

                break

            # else, add current information
            for col in d:

                d[col].append(ts_copy[col][idx])

        idx += 1

    return pd.DataFrame(d)

def assign_time(ts, start, increment):
    """
    Takes a time series without time stamps, the starting time (start),
    and the amount to be incremented by (increment) and returns an
    updated time series with the first column being named 'Times.'

    Assign time stamps to data points in a given time series. Assumed that start
    and increment are both integers. It is also assumed that no column holding
    times exists. start and increment can be negative or positive values.

    Author: River Veek
    """
    # START AND INCREMENT ARE INTS
    # DEFAULT FIRST COL NAME TO 'Times'

    # grab copy of ts (for preservation purposes)
    ts_copy = ts

    # for use in finding length of ts
    ts = ts.iloc[:, -1].tolist()  # create list holding all values (last col)
    times = []  # list to append times to
    total = 0  # total time units to add to

    # loop through ts and create times list
    for i in range(len(ts)):
        times.append(start + total)
        total += increment

    # reassign times column to ts and return
    ts_copy.insert(loc=0, column="Times", value=times)
    return ts_copy

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

def design_matrix(ts, data_start, data_end):
    """
    Takes a time series, float representing the size of input array,
    float representing the size of the output array, and returns a
    tuple that holds the two matrices (input matrix and output matrix,
    both as numpy arrays) in that particular order.

    Example of return:
    (input array, output array)

    data_start represents the size of the input matrix. data_end represents
    the size of the output matrix. Both parameters are expected to be floats
    but will immediately be converted into ints.
    """
    # input index == where to start input array, convert float -> int
    # ouput index == where to start output array, convert float -> int
    # return tuple of two numpy arrays containing

    # EXAMPLE RETURN VALUE
    # >>> design_matrix()
    # (([[1,2,3], [2,3,4], [3,4,5], ..., [9, 10, 11]], [[4,5], [5,6], [6,7], ..., [10, 11]]))

    # convert value col of ts to list
    ts_copy = ts.iloc[:, -1].tolist()

    # convert index args to ints (from floats)
    data_start = int(data_start)
    data_end = int(data_end)

    # create input matrix
    input = []

    # create output matrix
    output = []

    # loop through values in ts
    for i in range(len(ts_copy)):

        # tmp to be added to input matrix
        tmp = []

        # calculate input array
        for j in range(data_start):

            # don't access out of range elements
            if i + j >= len(ts_copy):
                break

            tmp.append(ts_copy[i + j])

        # only append row if it is
        #   - the same length as data_start
        #   - it leaves enough room to also add a corresponding output matrix
        #     as to not make it partially empty
        if len(tmp) == data_start and i + data_start + data_end <= len(ts_copy):
            input.append(tmp)

        # tmp to be added to output matrix
        tmp = []

        # calculate output array
        for j in range(data_end):

            # don't access out of range elements
            if i + j  + data_start >= len(ts_copy):
                break

            tmp.append(ts_copy[i + j + data_start])

        # only add tmp if it is full (same size as data_end)
        if len(tmp) == data_end:

            output.append(tmp)

    # convert input and output to numpy arrays, return
    input = np.array(input)
    output = np.array(output)

    return input, output

def logarithm(ts):
    """
    Converts values inside a dataframe (ts) to their
    log10 value, returns a timeseries with the new values.

    Calls: NA
    Called By:  TS_Tree.execute_tree()

    Author: Nick Titzler
    """

    nums = ts.iloc[:,-1,].to_list()


    # loop through value column, replace number with log10
    for i in range(len(nums)):
        item = nums[i]


        if item != 0:
            item = np.log10(nums[i]) # take log10
            #print(item)
            ts.iloc[:,-1,][i] = item
        elif (item == 0):
            #print(item)
            ts.iloc[:,-1,][i] = 0.0 # ignore if 0
        else:
            ts.iloc[:,-1,][i] = np.nan # keep nan as nan


    return ts



def cubic_root(ts):
    """
    Converts values inside a dataframe (ts) to the values
    cube root, returns a timeseries with the new values.

    Calls: NA
    Called By:  TS_Tree.execute_tree()

    Author: Nick Titzler
    """
    nums = ts.iloc[:,-1,].to_list()

    # loop through value column, replace val with cube root of val
    for i in range(len(nums)):
        item = nums[i]

        if item != 0:
            item = item**(1/3) # replace with cube root
            ts.iloc[:,-1,][i] = item
        elif (item == 0):
            ts.iloc[:,-1,][i] = 0.0  # ignore 0
        else:
            ts.iloc[:,-1,][i] = np.nan # ignore nan

    return ts

def split_data(ts, perc_training, perc_valid, perc_test):
    """
   splits ts dataframe into percentage sized arrays based on input percentages: perc_traning, perc_valid, and perc_test

   Calls: None
   Called By: ts2db()

    -[ts, ts, ts]
    -[perc_training, perc_valid, perc_test]

    """
    if (perc_training + perc_valid + perc_test) != 1:
        raise Exception("Error: percentages do not add to 1")

    p = np.array([perc_training, perc_valid, perc_test])
    a = np.array(ts.iloc[:,-1,].to_list())

    # check how many columns are in the dataset


    # first if branch for 1 column dataframes
    if len(ts.columns) == 1:

        length = len(a)
        values = np.split(a, (len(a)*p[:-1].cumsum()).astype(int)     )
        perc_training = pd.DataFrame(values[0])
        perc_valid = pd.DataFrame(values[1])
        perc_test = pd.DataFrame(values[2])
        return [perc_training, perc_valid, perc_test]

    else: # for two column dataframes

        res = []

        # iterate through columns, splitting data based on percentages
        for i in range(len(ts.columns)):

           col = np.array(ts.iloc[:,i].to_list())
           values = np.split(col, (len(col)*p[:-1].cumsum()).astype(int)) # split data into slices
           res.append(values)


        # create a dictionary that holds each percentage slice
        dictList = []
        for i in range(len(ts.columns)):
            dictList.append({})

        ctr = 0
        # combine relevant slices
        for i in range(len(ts.columns)):
            for j in range(len(ts.columns)):
                dictList[i][ts.columns[j]] = res[j][i]


        result = []

        # make each slice a dataframe, and return it
        for i in range(len(dictList)):
            x = pd.DataFrame.from_dict(dictList[i])
            result.append(x)



        return result


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
    train_db = design_matrix(ts_splits[0], input_index, output_index)       # CHANGE OUTPUT HANDLING
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
