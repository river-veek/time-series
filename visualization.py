"""

Author: Nick Titzler



"""

import preprocessing as pre
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


def plot(ts):
	if type(ts) == list:
		for item in ts:
			plt.plot(item)
		plt.show()
	else:
		plt.plot(ts)
		plt.show()

def histogram(ts):
    ts.plot.hist()
    plt.show()


def box_plot(ts):
    ts.boxplot()
    plt.show()

def normality_test(ts):
    pass

def mse(ts):
    pass
def mape(ts):
    pass
def smape(ts):
    pass
