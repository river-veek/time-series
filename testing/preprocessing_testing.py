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


#############################
# IMPUTE_MISSING_DATA() TESTS
#############################
def test_imp_miss_data():
    df2 = pd.DataFrame({'c1': [10, 11, "NaN"]})
    df3 = pd.DataFrame({'c1': ["NaN"]})
    df4 = pd.DataFrame({'c1': ["NaN", 10]})
    df5 = pd.DataFrame({'c1': [10, "NaN"]})
    df6 = pd.DataFrame({'c1': ["NaN", 11, 10]})
    df7 = pd.DataFrame({'c1': [10, "NaN", 11]})
    # df2 = impute_missing_data(df2)
    # df3 = impute_missing_data(df3)
    # df4 = impute_missing_data(df4)
    # df5 = impute_missing_data(df5)
    # df6 = impute_missing_data(df6)
    # df7 = impute_missing_data(df7)
    # print(df7)

#########################
# IMPUTE_OUTLIERS() TESTS
#########################

##############################
# LONGEST_CONTINUOUS_RUN TESTS
##############################
def test_long_cont_run():
    df2 = pd.DataFrame({'c1': [10, 11, "NaN"]})
    df3 = pd.DataFrame({'c1': ["NaN"]})
    df4 = pd.DataFrame({'c1': ["NaN", 10, 9]})
    df5 = pd.DataFrame({'c1': [10, "NaN"]})
    df6 = pd.DataFrame({'c1': ["NaN", 11, 10, 12, 11, 9]})
    df7 = pd.DataFrame({'c1': [10, "NaN", 11]})


###############
# CLIP() TESTS
###############

#####################
# ASSIGN_TIME() TESTS
#####################

##################
# SCALING() TESTS
##################

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
	df_actual_output = standardize(df_test_input)
	assert list(df_actual_output.iloc[:, -1]) == list(df_test_output.iloc[:, -1])


##########################
# LOGARITHM TESTS
##########################

def test_logarithm():
	"""
	Tests 1 column dataframe
	"""
	ts = pd.DataFrame({
		"Times": [0, 1, 2, 3, 4, 5],
		"Values": [1.0, 0.0, 9.0, 10.0, 8.0, 4.0]
	})

	logarithm(ts)


##########################
# CUBIC ROOT TESTS
##########################

def test_cubic_root():

	ts = pd.DataFrame({
		"Times": [0, 1, 2, 3, 4, 5],
		"Values": [1.0, 0.0, 9.0, 10.0, 8.0, 4.0]
	})

	df = cubic_root(ts)

##########################
# SPLIT DATA TESTS
##########################

def test_split_data():
	ts = pd.DataFrame({
		"Times": [0, 1, 2, 3, 4, 5],
		"Values": [1.0, 0.0, 9.0, 10.0, 8.0, 4.0]
	})

	val1 = .25
	val2 = .50
	val3 = .25

	split_data(ts, val1, val2, val3)


