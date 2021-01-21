"""
Preprocessing Functions
"""

from time_series import TimeSeries


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
