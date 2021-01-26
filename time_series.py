"""
TimeSeries Class

Author: Nick Titzler

Notes: TimeSeries class contains a dictionary where the key is the time stamp of the data,
and the value is the magnitude for said data. If there are multiple descriptor coloumns,
they will be seperated in the dictionary with a comma.

ex.
{"string":float}
{"01/27/1998,00:24:00": 12.0, "01/27/1998,00:48:00": 24.2}

if no timestamp is provided, the key will be given a string value counting up

ex. 
{"1":28.3}

"""

import numpy as np




class TimeSeries:

	def __init__(self):
		self.series = {}


	def mean(self):
		"""
		return the mean of the series
		"""

		temp = []
		for item in self.series.items():
			temp.append(item[1])

		
		return np.mean(temp)


	def stddiv(self):
		"""
		return standard div of time series
		"""
		temp = []
		for item in self.series.items():
			temp.append(item[1])

		return np.std(temp)
		




