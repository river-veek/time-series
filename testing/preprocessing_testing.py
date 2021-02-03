"""
Tests for preprocessing.py methods.

To run nosetests (from 'time-series/' directory):

    nosetests -v testing/preprocessing_testing.py


Author(s): Nick Titzler, River Veek
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
def test_NaN_last_impute_missing_data():
    """
    Testing impute_missing_data() with NaN as last value and as first value.
    """
    df1 = pd.DataFrame({'Time': [0, 1, 2], 'Daily Top': ["GME", "AMC", "BB"], 'Vals': [14.6, 17.8, "NaN"]})
    df2 = pd.DataFrame({'Time': [0, 1, 2], 'Daily Top': ["GME", "AMC", "BB"], 'Vals': [14.6, 17.8, 16.2]})

    df3 = pd.DataFrame({'Time': [0, 1, 2], 'Daily Top': ["GME", "AMC", "BB"], 'Vals': ["NaN", 10, 11]})
    df4 = pd.DataFrame({'Time': [0, 1, 2], 'Daily Top': ["GME", "AMC", "BB"], 'Vals': [10.5, 10, 11]})

    assert impute_missing_data(df1).equals(df2)
    assert impute_missing_data(df3).equals(df4)

def test_NaN_middle_impute_missing_data():
    """
    Testing impute_missing_data() with NaN as a middle value (not the first or last value).
    """
    df1 = pd.DataFrame({'Time': [0, 1, 2], 'Vals': [10, "NaN", 20]})
    df2 = pd.DataFrame({'Time': [0, 1, 2], 'Vals': [10.0, 15.0, 20.0]})

    assert impute_missing_data(df1).equals(df2)

def test_NaN_only_impute_missing_data():
    """
    Testing impute_missing_data() with NaN as only value.
    """
    df1 = pd.DataFrame({'Time': [0], 'Vals': ["NaN"]})
    df2 = pd.DataFrame({'Time': [0], 'Vals': [0]})

    assert impute_missing_data(df1).equals(df2)

def test_no_NaN_impute_missing_data():
    """
    Testing impute_missing_data() with no NaN.
    """
    df1 = pd.DataFrame({'Time': [0], 'Vals': [22]})
    df2 = pd.DataFrame({'Time': [0], 'Vals': [22]})

    assert impute_missing_data(df1).equals(df2)

#########################
# IMPUTE_OUTLIERS() TESTS
#########################
def test_outlier_first_impute_outliers():
    """
    Testing impute_outliers() with outlier as first value.
    """
    df1 = pd.DataFrame({'Time': [0, 1, 2, 3, 4, 5], 'Daily Top': ["GME", "AMC", "BB", "DOGE", "NOK", "BTC"],
                        'Vals': [420, 17.8, 15, 1, 25, 17]})
    df2 = pd.DataFrame({'Time': [0, 1, 2, 3, 4, 5], 'Daily Top': ["GME", "AMC", "BB", "DOGE", "NOK", "BTC"],
                        'Vals': [16.4, 17.8, 15, 1, 25, 17]})

    assert impute_outliers(df1).equals(df2)

def test_outlier_last_impute_outliers():
    """
    Testing impute_outliers() with outlier as last value.
    """
    df1 = pd.DataFrame({'Time': [0, 1, 2, 3, 4, 5], 'Daily Top': ["GME", "AMC", "BB", "DOGE", "NOK", "BTC"],
                        'Vals': [5, 17.8, 15, 1, 25, 420]})
    df2 = pd.DataFrame({'Time': [0, 1, 2, 3, 4, 5], 'Daily Top': ["GME", "AMC", "BB", "DOGE", "NOK", "BTC"],
                        'Vals': [5, 17.8, 15, 1, 25, 13]})

    assert impute_outliers(df1).equals(df2)

def test_outlier_middle_impute_outliers():
    """
    Testing impute_outliers() outlier as a middle value (not the first or last value).
    """
    df1 = pd.DataFrame({'Time': [0, 1, 2, 3, 4, 5], 'Daily Top': ["GME", "AMC", "BB", "DOGE", "NOK", "BTC"],
                        'Vals': [5, 17.8, 15, 420, 25, 1]})
    df2 = pd.DataFrame({'Time': [0, 1, 2, 3, 4, 5], 'Daily Top': ["GME", "AMC", "BB", "DOGE", "NOK", "BTC"],
                        'Vals': [5, 17.8, 15, 20, 25, 1]})

    assert impute_outliers(df1).equals(df2)

def test_no_outlier_impute_outliers():
    """
    Testing impute_outliers() with no oulier.
    """
    df1 = pd.DataFrame({'Time': [0, 1, 2, 3, 4, 5], 'Daily Top': ["GME", "AMC", "BB", "DOGE", "NOK", "BTC"],
                        'Vals': [5, 17.8, 15, 16, 25, 1]})
    df2 = pd.DataFrame({'Time': [0, 1, 2, 3, 4, 5], 'Daily Top': ["GME", "AMC", "BB", "DOGE", "NOK", "BTC"],
                        'Vals': [5, 17.8, 15, 16, 25, 1]})

    assert impute_outliers(df1).equals(df2)

def test_multiple_outlier_impute_outliers():
    """
    Testing impute_outliers() with multiple outliers.
    """
    df1 = pd.DataFrame({'Time': [0, 1, 2, 3, 4, 5, 6, 7, 8, 9],
                        'Daily Top': ["GME", "AMC", "BB", "DOGE", "NOK", "BTC", "NIO", "DIS", "ETH", "JD"],
                        'Vals': [10, 17.8, 15, 16, 25, 17, 18, 19, 500, 700]})
    df2 = pd.DataFrame({'Time': [0, 1, 2, 3, 4, 5, 6, 7, 8, 9],
                        'Daily Top': ["GME", "AMC", "BB", "DOGE", "NOK", "BTC", "NIO", "DIS", "ETH", "JD"],
                        'Vals': [10, 17.8, 15, 16, 25, 17, 18, 19, 24.3203125, 29.640625]})
                        # last test repeats until no outliers are found
                        # values for each iteration are shown below
                        # 10, 17.8, 15, 16, 25, 17, 18, 19, 359.5, 189.25
                        # 10, 17.8, 15, 16, 25, 17, 18, 19, 104.125, 61.5625
                        # 10, 17.8, 15, 16, 25, 17, 18, 19, 40.28125, 29.640625
                        # 10, 17.8, 15, 16, 25, 17, 18, 19, 24.3203125, 29.640625

    assert impute_outliers(df1).equals(df2)

##############################
# LONGEST_CONTINUOUS_RUN TESTS
##############################
def test_longest_continuous_run():
    """
    Testing longest_continuous_run().
    """
    df1 = pd.DataFrame({'Time': [0, 1, 2, 3, 4, 5, 6, 7, 8, 9],
                        'Daily Top': ["GME", "AMC", "BB", "DOGE", "NOK", "BTC", "NIO", "DIS", "ETH", "JD"],
                        'Vals': [10, 17.8, 15, "NaN", 25, 17, 18, 19, 500, 700]})
    df2 = pd.DataFrame({'Time': [4, 5, 6, 7, 8, 9],
                        'Daily Top': ["DOGE", "NOK", "BTC", "NIO", "DIS", "ETH", "JD"],
                        'Vals': [ 25, 17, 18, 19, 500, 700]})

    # FIXME: need to trim ALL columns in DF, not just value column
    assert longest_continuous_run(df1).equals(df2)

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
		"greetings": ["hello", "hello1", "hello2", "hello3", "hello4", "hello5"],
		"date": ["monday", "tue", "wed", "thu", "friday", "saturday"],
		"Values": [1.0, 0.0, 9.0, 10.0, 8.0, 4.0]
	})
	ts2 = pd.DataFrame({
		"Values": [1.0, 0.0, 9.0, 10.0, 8.0, 4.0]
	})

	val1 = .25
	val2 = .50
	val3 = .25
	#ts = logarithm(ts)
	ts = cubic_root(ts)
	res = split_data(ts, val1, val2, val3)


	split_data(ts, val1, val2, val3)
