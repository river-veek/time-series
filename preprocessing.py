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
