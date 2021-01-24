"""
File IO functions

Author: Nick Titzler
"""
import csv
import pickle

#for testing


def read_from_file(input_file_name):
	# possible read in formats can be csv, pickle, parquet?

	#for testing
	path = "timeSeriesData/TimeSeriesData2/"
	path = path + input_file_name

	
	result = []


	#csv read in
	with open(path, newline='') as csvfile:
		data = csv.reader(csvfile, delimiter=' ', quotechar='|')
		for row in data:
			if len(row[0].split(",")) != 1:
				result.append(row[0].split(","))
			else:
				result.append(row[0])

	return result

def write_to_file(output_file_name):
    pass


def test():
	fname1 = "1_temperature_test.csv"
	fname2 = "WindSpeed2010Jan20mMin.csv"
	read_from_file(fname2)

test()