"""

Author: Nick Titzler



"""

import preprocessing as pre
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy import stats
from sklearn.metrics import mean_squared_error



#########################
  # HELPER FUNCTIONS
#########################

def fiveNumberSummary(ts):
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
	ax = ts.plot()
	ts.plot.hist(ax=ax, orientation="horizontal")
	plt.show()

	if type(fname) == str:
		plt.savefig(fname)

	return ts

def box_plot(ts, fname=None):
	if type(ts) == list:
		for item in ts:
			item.boxplot()
			fiveNumberSummary(item)
		plt.show()

	else:
		ts.boxplot()
		
		fiveNumberSummary(ts)
		plt.show()

	if type(fname) == str:
		plt.savefig(fname)
	
	return ts


def normality_test(ts):
	return stats.normaltest(ts)

def mse(y_forecast, y_test: str):
	yf = db2ts(y_forecast)
	yt = read_from_file(y_test)

    return mean_squared_error(yf.iloc[:,-1].to_numpy(), yt.iloc[:,-1].to_numpy())

def mape(y_forecast, y_test: str):
	yf = db2ts(y_forecast)
	yt = read_from_file(y_test)

    return np.mean((np.abs(yf.iloc[:,-1].to_numpy()-yt.iloc[:,-1].to_numpy()) / yf.iloc[:,-1].to_numpy())) * 100

def smape(y_forecast, y_test: str):

	yf = db2ts(y_forecast)
	yt = read_from_file(y_test)
	
    return 100/len(yf.iloc[:,-1].to_numpy()) * np.sum(2 * np.abs(yt.iloc[:,-1].to_numpy() - yf.iloc[:,-1].to_numpy()) / (np.abs(yf.iloc[:,-1].to_numpy()) + np.abs(yt.iloc[:,-1].to_numpy())))




