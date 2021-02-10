"""
----------------------------------------------------------------------------------------
Contains Modeling and Forecasting Functions

Author - Cameron Jordal
Group - Keyboard Warriors
Last Modified - 2/9/21
----------------------------------------------------------------------------------------
"""

from sklearn.neural_network import MLPRegressor
import file_io as fio
import preprocessing as pp
import numpy as np


#######################
# HELPER FUNCTIONS
#######################

def mlp_window_selector(data, num_divs=5):
    """
    Function that a set of data and automatically
    selects an appropriate range to view the values.
    """
    # convert the first aspect of data back into time series
    # to be analyzed
    ts_data = pp.db2ts(data[0])
    # get mean of data
    mean_val = ts_data.mean()
    # get standard deviation of data
    std_val = ts_data.std()
    # return window of num_divs standard deviations from mean
    min_val = mean_val - std_val * num_divs
    max_val = mean_val + std_val * num_divs
    return (float(min_val), float(max_val))

def mlp_input_mapper(data, window):
    """
    Function that takes a range of input data
    defined from in a tuple window and squashes
    it into a range of 0 to 1.
    """
    # get factor to scale data by
    mult = 1 / (window[1] - window[0])
    # return scaled data with minimum value offset
    return mult * (data - window[0])

def mlp_output_mapper(data, window):
    """
    Function that takes a range of input data
    in a range of 0 to 1 and expands it into a
    range defined in the tuple window.
    """
    # get factor to scale data by
    mult = window[1] - window[0]
    # return scaled data offset by minimum value
    return mult * data + window[0]


###################
# FUNCTIONS
###################

def mlp_model(train, layers=(100,), window_size=5):
    """
    Takes in a tuple of 2 numpy matrices, a tuple of layers,
    and an integer. Returns tuple with a MLPRegressor model and
    a tuple.

    Creates a multi-layer perceptron model with a provided number
    of hidden layers. Trains the model with provided data.
    """
    # generate a window
    window = mlp_window_selector(train, window_size)
    # interpolate new data
    train_x = mlp_input_mapper(train[0], window)
    train_y = mlp_input_mapper(train[1], window)
    # generate model
    model = MLPRegressor(hidden_layer_sizes=tuple(layers))
    # fit model with new rounded data
    model.fit(train_x, train_y)
    # return model and window
    return (model, window)

def mlp_forecast(model_data, x_filename):
    """
    Takes in a tuple containing a MLPRegressor object and a tuple as
    well a string. Returns a numpy matrix.

    Predicts a future set of values from a given set of values
    and a trained model.
    """
    # extract model and tree from model data
    model = model_data[0]
    window = model_data[1]
    # grab test data from file
    x = fio.read_from_file(x_filename)
    x = x.to_numpy()
    # predict values
    y_hat = model.predict(x)
    # interpolate predicted values to real size
    y_hat = mlp_output_mapper(y_hat, window)
    return y_hat
