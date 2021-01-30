"""
Tests for time_series.py containing the time series class

Author: Nick Titzler

To run nosetests (from 'time-series/' directory):

    nosetests testing/preprocessing_testing.py

"""
import numpy as np
import sys
sys.path.append("../")
import file_io as fio
from preprocessing import *
import nose


'''
def test1_timeSeriesData1():
	"""
	test time series creation from timeSeriesData1 files

	"""
	fileNames = ["1_temperature_test.csv","1_temperature_train.csv","2_temperature_subsampled_test.csv",
	"2_temperature_subsampled_train.csv", "3_passengers_test.csv","3_passengers_train.csv","4_irradiance_test.csv",
	"4_irradiance_train.csv", "5_irradiance_subsampled_test.csv", "5_irradiance_subsampled_train.csv", "6_sunspots_test.csv", "6_sunspots_train.csv",
	"7_distribution_subsampled_norm_test.csv", "7_distribution_subsampled_norm_train.csv", "8_distribution_subsampled_test.csv", "8_distribution_subsampled_train.csv"]


	fname = "../timeSeriesData/TimeSeriesData1/"+fileNames[0]

	ts = fio.read_from_file(fname)
	#logarithm(ts)
'''


#######################
# SCALING() TESTS
#######################

def test_general_scaling():
	"""
	Test general use case of scaling function
	"""
	test_input = {
		"Times": [0, 1, 2, 3, 4, 5],
		"Values": [1, 0, 9, 10, 8, 4]
	}
	df_test_input = pd.DataFrame(test_input)
	test_output = {
		"Times": [0, 1, 2, 3, 4, 5],
		"Values": [0.1, 0, .9, 1, .8, .4]
	}
	df_test_output = pd.DataFrame(test_output)
	df_actual_output = scaling(df_test_input)
	assert list(df_actual_output.iloc[:, -1]) == list(df_test_output.iloc[:, -1])

def test_negative_scaling():
	"""
	General test case with both negative and positive values to be scaled
	"""
	test_input = {
		"Times": [0, 1, 2, 3, 4, 5],
		"Values": [-1, 0, -5, 1, 4, -2]
	}
	df_test_input = pd.DataFrame(test_input)
	test_output = {
		"Times": [0, 1, 2, 3, 4, 5],
		"Values": [0.2, 0, 1, 0.2, 4/5, 2/5]
	}
	df_test_output = pd.DataFrame(test_output)
	df_actual_output = scaling(df_test_input)
	assert list(df_actual_output.iloc[:, -1]) == list(df_test_output.iloc[:, -1])

def test_same_scaling():
	"""
	Test case where all values are identical
	"""
	test_input = {
		"Times": [0, 1, 2],
		"Values": [3, 3, 3]
	}
	df_test_input = pd.DataFrame(test_input)
	test_output = {
		"Times": [0, 1, 2],
		"Values": [1, 1, 1]
	}
	df_test_output = pd.DataFrame(test_output)
	df_actual_output = scaling(df_test_input)
	assert list(df_actual_output.iloc[:, -1]) == list(df_test_output.iloc[:, -1])

def test_min_scaling():
	"""
	Test case where all values are 0
	"""
	test_input = {
		"Times": [0, 1, 2],
		"Values": [0, 0, 0]
	}
	df_test_input = pd.DataFrame(test_input)
	test_output = {
		"Times": [0, 1, 2],
		"Values": [0, 0, 0]
	}
	df_test_output = pd.DataFrame(test_output)
	df_actual_output = scaling(df_test_input)
	assert list(df_actual_output.iloc[:, -1]) == list(df_test_output.iloc[:, -1])

def test_empty_scaling():
	"""
	Test case where there are no entries to be scaled
	"""
	test_input = {
		"Times": [],
		"Values": []
	}
	df_test_input = pd.DataFrame(test_input)
	test_output = {
		"Times": [],
		"Values": []
	}
	df_test_output = pd.DataFrame(test_output)
	df_actual_output = scaling(df_test_input)
	assert list(df_actual_output.iloc[:, -1]) == list(df_test_output.iloc[:, -1])

def test_monocolumn_scaling():
	"""
	Test case where only one column is provided
	"""
	test_input = [1, 0, 9, 10, 8, 4]
	df_test_input = pd.DataFrame(test_input)
	test_output = [0.1, 0, .9, 1, .8, .4]
	df_test_output = pd.DataFrame(test_output)
	df_actual_output = scaling(df_test_input)
	assert list(df_actual_output.iloc[:, -1]) == list(df_test_output.iloc[:, -1])

def test_multicolumn_scaling():
	"""
	Test case where there are multiple columns provided
	"""
	test_input = {
		"Months": [0, 1, 2, 3, 4, 5],
		"Days": [12, 1, 6, 24, 20, 18],
		"Values": [1, 0, 9, 10, 8, 4]
	}
	df_test_input = pd.DataFrame(test_input)
	test_output = {
		"Months": [0, 1, 2, 3, 4, 5],
		"Days": [12, 1, 6, 24, 20, 18],
		"Values": [0.1, 0, .9, 1, .8, .4]
	}
	df_test_output = pd.DataFrame(test_output)
	df_actual_output = scaling(df_test_input)
	assert list(df_actual_output.iloc[:, -1]) == list(df_test_output.iloc[:, -1])


##########################
# STANDARDIZE() TESTS
##########################

def test_general_standardize():
	"""
	Test the general use case of the standardize function
	"""
	test_input = {
		"Times": [0, 1, 2, 3, 4, 5],
		"Values": [1, 0, 9, 10, 8, 4]
	}
	df_test_input = pd.DataFrame(test_input)
	input_mean = df_test_input.iloc[:, -1].mean()
	input_std = df_test_input.iloc[:, -1].std()
	test_output = {
		"Times": [0, 1, 2, 3, 4, 5],
		"Values": [
			(1 - input_mean) / input_std,
			(0 - input_mean) / input_std,
			(9 - input_mean) / input_std,
			(10 - input_mean) / input_std,
			(8 - input_mean) / input_std,
			(4 - input_mean) / input_std
		]
	}
	df_test_output = pd.DataFrame(test_output)
	print("Expected:")
	print(df_test_output)
	df_actual_output = standardize(df_test_input)
	print("Got:")
	print(df_actual_output)
	assert list(df_actual_output.iloc[:, -1]) == list(df_test_output.iloc[:, -1])

'''
def main():
	test1_timeSeriesData1()
	#test2_timeSeriesData2()
	pass

main()
'''