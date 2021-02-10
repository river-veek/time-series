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
	"""
		Takes a string input as the name of a file, returns a dataframe containing the file

		Author: Nick Titzler
	"""

	# use csv file
	data = pd.read_csv(input_file_name, na_values=['NaN'])

	df = pd.DataFrame(data)

	return df


def write_to_file(ts, output_file_name):
	"""
		Takes a time series, and a string with the name of the output file. Returns None, and
		writes a csv file to output_file_name

		Author: Nick Titzler
	"""
	path = "output/" + output_file_name

	# write dataframe to file.
	df.to_csv(path, index=1)




