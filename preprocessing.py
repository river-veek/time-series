"""
Preprocessing Functions
"""

########################
# IMPORTS AND GLOBALS
########################

from time_series import TimeSeries

######################
# HELPER FUNCTIONS
######################

def get_magnitudes(ts):
    """
    Takes in an a time series and returns a time series.

    Creates a new time series with the each value being the magnitude
    of the provided time series values.
    """
    new_ts = TimeSeries()
    for val in ts:
        new_ts.append(abs(val))


######################
# HELPER FUNCTIONS
######################

def denoise(ts):
    pass

def impute_missing_data(ts):
    """
    Takes a time series and returns a new time series.

    Compute missing data point by taking mean of
    adjacent points in time. Only one data point is
    assumed to be missing.
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
    subset run as a new time series.
    """
    new_ts = TimeSeries()
    longest_run = 0
    cur_run = 0
    cur_idx = 0
    start_idx = 0
    end_idx = 0

    # WORKS WITH MULTIPLE MISSING POINTS

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

def difference(ts):
    """
    Takes in an a time series and returns a time series.

    Creates a new time series with the each value being the magnitude
    of the difference between each consecutive element of the provided
    time series.
    """
    new_ts = TimeSeries()
    for val_id in range(len(ts)):
        new_val = ts[val_id+1] - ts[val_id]
        new_ts.append(new_val)
    return new_ts


def scaling(ts):
    """
    Takes in a time series and returns a time series.

    Creates a new time series in which the magnitudes of each time series
    value is compressed into the range of [0, 1].
    """
    new_ts = TimeSeries()
    ts_max = ts.max()
    for val in ts:                  # CURRENTLY ASSUMING MAX != 0
        new_ts.append(val/ts_max)


def standardize(ts):
    """
    Takes in a time series and returns a time series.

    Creates a new time series that translates the values of the existing
    time series to have a mean of 0 and a variance of 1.
    """
    new_ts = TimeSeries()
    ts_mu = ts.mean()
    ts_sig = ts.stddiv()
    for val in ts:
        new_val = (val - ts_mu) / ts_sig
        new_ts.append(new_val)
