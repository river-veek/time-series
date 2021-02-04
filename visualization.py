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


def plot(ts):
	if type(ts) == list:
	 	for item in ts:
	 		print(item)
	 		plt.plot(item)
	 	plt.show()
	else:
		plt.plot(ts)
		plt.show()

	# handle file saving
	if (save == True) and type(fname) == str:
		plt.savefig(fname)

def histogram(ts, save=False, fname=None):
	if type(ts) == list:
	 	for item in ts:
	 		item.plot.hist()
	 	plt.show()
	else:
		ts.plot.hist()
		plt.show()

	if (save == True) and type(fname) == str:
		plt.savefig(fname)

def box_plot(ts, save=False, fname=None):
	if type(ts) == list:
		for item in ts:
			item.boxplot()
			fiveNumberSummary(item)
		plt.show()

	else:
		ts.boxplot()
		
		fiveNumberSummary(ts)
		plt.show()

	if (save == True) and type(fname) == str:
		plt.savefig(fname)
	


def normality_test(ts):
	return stats.normaltest(ts)

def mse(y_test: np.array, y_forecast: np.array): 
    return mean_squared_error(y_test, y_forecast)

def mape(y_test: np.array, y_forecast: np.array):
    return np.mean((np.abs(y_test-y_forcast) / y_test)) * 100

def smape(y_test: np.array, y_forecast: np.array):
    return 100/len(y_test) * np.sum(2 * np.abs(y_forecast - y_test) / (np.abs(y_test) + np.abs(y_forecast)))




