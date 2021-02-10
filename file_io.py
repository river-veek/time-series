"""
----------------------------------------------------------------------------------------
Contains File I/O functions.

Author - Nick Titzler
Group - Keyboard Warriors
Last Modified - 2/9/21
----------------------------------------------------------------------------------------
"""
import csv
import pickle
import pandas as pd
import numpy as np
#for testing


def read_from_file(input_file_name):

	# use csv file
	data = pd.read_csv(input_file_name, na_values=['NaN'])

	df = pd.DataFrame(data)

	return df


def write_to_file(ts, output_file_name):
	"""
		writes a time series to a file

		BUG: currently program writes a 0 to the start of the file, unsure as to why
	"""
	path = "write_to_file_outputTesting/" + output_file_name

	# write dataframe to file.
	df.to_csv(path, index=1)



def test():
	fname1 = "1_temperature_test.csv"
	fname2 = "wind_cointzio_10m_complete.csv"
	#read_from_file(fname1)

#test()
