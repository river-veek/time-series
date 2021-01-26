"""
File IO functions

Author: Nick Titzler
"""
import csv
import pickle
import time_series as TS

#for testing


def read_from_file(input_file_name):
	"""
	Takes input of a file name

	Returns a instance of a TimeSeries Class


	NEED TO CHANGE: only currently works with timeSeries1 datasets
	"""
	ts = TS.TimeSeries()
	result = []


	# check if the file exists
	try:
		with open(input_file_name, "r") as f:
			pass
	except:
		print("File does not currently exist, now exiting")
		



	#csv read in
	with open(input_file_name, newline='') as csvfile:
		csvfile.readline()
		data = csv.reader(csvfile, delimiter=' ', quotechar='|')

		for row in data:
			if len(row[0].split(",")) != 1:
				result.append(row[0].split(","))
			else:
				result.append(row[0])
	
	

	for i in range(len(result)):
		ts.series[str(i)] = float(result[i])




	return ts

def write_to_file(output_file_name):
	return 0


def test():
	fname1 = "1_temperature_test.csv"
	fname2 = "wind_cointzio_10m_complete.csv"
	#read_from_file(fname1)

#test()