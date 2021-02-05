"""
Modeling and Forecasting Functions
"""

from sklearn.neural_network import MLPClassifier
import file_io as fio


def mlp_model(train, layers=(100,)):
    """
    Creates a multi-layer perceptron model with a provided number
    of hidden layers. Trains the model with provided data.
    """
    model = MLPClassifier(hidden_layer_sizes=tuple(layers))
    model.fit(train[0], train[1])
    return model

def mlp_forecast(model, x_filename):
    """
    Predicts a future set of values from a given set of values
    and a trained model.
    """
    x = fio.read_from_file(x_filename)
    x = x.to_numpy()
    y_hat = model.predict(x)
    return y_hat
