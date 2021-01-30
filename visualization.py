"""

Author: Nick Titzler



"""

import preprocessing as pre
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt



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
	 		plt.plot(item)
	 	plt.show()
	else:
		plt.plot(ts)
		plt.show()

def histogram(ts):
	if type(ts) == list:
	 	for item in ts:
	 		item.plot.hist()
	 	plt.show()
	else:
		ts.plot.hist()
		plt.show()

def box_plot(ts):
	if type(ts) == list:
		for item in ts:
			item.boxplot()
			fiveNumberSummary(item)
		plt.show()



	else:
		ts.boxplot()
		
		fiveNumberSummary(ts)
		plt.show()

	# print five number summary
	


def normality_test(ts):
    pass

def mse(ts):
    pass
def mape(ts):
    pass
def smape(ts):
    pass
