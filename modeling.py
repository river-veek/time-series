"""
Modeling and Forecasting Functions
"""

from sklearn.neural_network import MLPClassifier


def mlp_model(layers=(100,)):
    """
    Creates a multi-layer perceptron model with a provided number
    of hidden layers.
    """
    model = MLPClassifier(hidden_layer_sizes=layers)
    return model

def mlp_fit(model, x_train, y_train):
    """
    Trains a multi-layer perceptron model on a provided
    training set.
    """
    model.fit(x_train, y_train)
    return model

def forecast(model, x):
    """
    Predicts a future set of values from a given set of values
    and a trained model.
    """
    y_hat = model.predict(x)
    return y_hat
