"""
----------------------------------------------------------------------------------------
Contains the plotting functions, and MSE, MAPE, SMAPE,
and normalization tests.

Author - Nick Titzler
Group - Keyboard Warriors
Last Modified - 2/9/21
----------------------------------------------------------------------------------------
"""

import preprocessing as pre
import file_io as fio
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy import stats
from sklearn.metrics import mean_squared_error



#########################
  # HELPER FUNCTIONS
#########################

def fiveNumberSummary(ts):
	"""
	Creates a five number summary from the dataframe input ts
	"""
	quartiles = np.percentile(ts.iloc[:,-1,], [25, 50, 75])
	print("~~~~FIVE NUMBER SUMMARY~~~~~")
	print("		Min:	",ts.iloc[:,-1,].min())
	print("		Q1:		",quartiles[0])
	print("		Mean:	",quartiles[1])
	print("		Q3:		",quartiles[2])
	print("		Max:	",ts.iloc[:,-1,].max())


#########################
  # GRAPHING FUNCTIONS
#########################


def plot(ts, fname=None):
	"""
	Creates a plot of ts. If ts is given as a list, it will plot all ts's in the list.

	Author: Nick Titzler
	"""

	if type(ts) == list:
		for item in ts:
			item.plot()
		plt.show()
	else:
		ts.plot()
		plt.show()

	# handle file saving
	if type(fname) == str:
		plt.savefig(fname)

	return ts

def histogram(ts, fname=None):
	"""
	Creates a histogram of the dataframe ts and displays it.

	Author: Nick Titzler
	"""
	ax = ts.plot()
	ts.plot.hist(ax=ax, orientation="horizontal")
	plt.show()

	if type(fname) == str:
		plt.savefig(fname)

	return ts

def box_plot(ts, fname=None):
	"""
	Creates a boxplot of the dataframe ts and displays it. 
	Prints a five number summary of the data.

	Author: Nick Titzler
	"""
	fiveNumberSummary(ts)
	x = ts.iloc[:,-1]


	plt.boxplot(x)
	plt.show()

	if type(fname) == str:
		plt.savefig(fname)

	return ts


def normality_test(ts):
	"""
	runs a normality test on a timeseries
	
	Author: Nick Titzler
	"""
	return stats.normaltest(ts)

def mse(y_forecast, y_test: str):
	"""
	takes in a database (y_forcast) and a file name (y_test: str)
	and returns the mean squared error between the datasets

	Author: Nick Titzler
	"""
	yf = pre.db2ts(y_forecast)
	yt = fio.read_from_file(y_test)
	return mean_squared_error(yf.iloc[:,-1].to_numpy(), yt.iloc[:,-1].to_numpy())

def mape(y_forecast, y_test: str):
	"""
	takes in a database (y_forcast) and a file name (y_test)
	and returns the mean absoulute percentage error

	Author: Nick Titzler
	"""
	yf = pre.db2ts(y_forecast)
	yt = fio.read_from_file(y_test)
	return np.mean((np.abs(yf.iloc[:,-1].to_numpy()-yt.iloc[:,-1].to_numpy()) / yf.iloc[:,-1].to_numpy())) * 100

def smape(y_forecast, y_test: str):
	"""
	takes in a database (y_forcast) and a file name (y_test)
	and returns the symmetric mean absolute percentage error

	Author: Nick Titzler
	"""
	yf = pre.db2ts(y_forecast)
	yt = fio.read_from_file(y_test)
	return 100/len(yf.iloc[:,-1].to_numpy()) * np.sum(2 * np.abs(yt.iloc[:,-1].to_numpy() - yf.iloc[:,-1].to_numpy()) / (np.abs(yf.iloc[:,-1].to_numpy()) + np.abs(yt.iloc[:,-1].to_numpy())))
