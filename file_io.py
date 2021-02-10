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
		Checks to see if the file name is 

		Author: Nick Titzler
	"""
	
	# try to read in csv file
	try:
		data = pd.read_csv(input_file_name, na_values=['NaN'])
		df = pd.DataFrame(data)
		return df
	# if not a csv open it as a pickle
	except: 
		try:
			data = pickle.load( open(input_file_name, "rb" ) )
			df = pd.DataFrame.from_dict(data)
			return df
	
		except: # if its neither, exit the program, or if the file is empty

			print("File type not accepted It is empty or it is not using .csv, .p, or .pkl\n\n")
			exit()

	


def write_to_file(ts, output_file_name):
	"""
		Takes a time series, and a string with the name of the output file. Returns None, and
		writes a csv file to output_file_name

		Author: Nick Titzler
	"""
	path = "output/" + output_file_name

	# write dataframe to file.
	ts.to_csv(path, index=1)




