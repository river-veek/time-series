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

	#for testing
	path = "timeSeriesData/TimeSeriesData1/"
	path = path + input_file_name
	ts = TS.TimeSeries()

	
	result = []


	#csv read in
	with open(path, newline='') as csvfile:
		data = csv.reader(csvfile, delimiter=' ', quotechar='|')

		for row in data:
			if len(row[0].split(",")) != 1:
				result.append(row[0].split(","))
			else:
				result.append(row[0])
	
	

	for i in range(len(result)):

		if result[i] == "\ufeff28.4":
			
			continue

		ts.series[str(i)] = float(result[i])



	print(ts.series)




	return result

def write_to_file(output_file_name):
	return 0


def test():
	fname1 = "1_temperature_test.csv"
	fname2 = "wind_cointzio_10m_complete.csv"
	read_from_file(fname1)

test()