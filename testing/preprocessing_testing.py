"""
----------------------------------------------------------------------------------------
Tests and Testing Instructions for preprocessing.py

Authors - River Veek, Nick Titzler, Cameron Jordal
Group - Keyboard Warriors
Last Modified - 2/9/2021
----------------------------------------------------------------------------------------


----------------------------------------------------------------------------------------
To run all nosetests (from 'time-series/' directory):

    nosetests -v testing/preprocessing_testing.py

To run single test class:

    nosetests -v testing/preprocessing_testing.py:<class name>

To run single test module (single test from within a class):

    nosetests -v testing/preprocessing_testing.py:<class name>.<module name>
----------------------------------------------------------------------------------------
"""

import numpy as np
import sys
sys.path.append("../")
import file_io as fio
from preprocessing import *
import nose
import numpy as np






#############################
# IMPUTE_MISSING_DATA() TESTS
#############################
class Test_impute_missing_data:
    """Test class for impute_missing_data()."""
    def test_NaN_last_impute_missing_data(self):
        """
        Testing impute_missing_data() with NaN as last value and as first value.
        """
        df1 = pd.DataFrame({'Time': [0, 1, 2], 'Daily Top': ["GME", "AMC", "BB"], 'Vals': [14.6, 17.8, np.nan]})
        df2 = pd.DataFrame({'Time': [0, 1, 2], 'Daily Top': ["GME", "AMC", "BB"], 'Vals': [14.6, 17.8, 16.2]})

        df3 = pd.DataFrame({'Time': [0, 1, 2], 'Daily Top': ["GME", "AMC", "BB"], 'Vals': [np.nan, 10, 11]})
        df4 = pd.DataFrame({'Time': [0, 1, 2], 'Daily Top': ["GME", "AMC", "BB"], 'Vals': [10.5, 10, 11]})

        assert impute_missing_data(df1).equals(df2)
        assert impute_missing_data(df3).equals(df4)

    def test_NaN_middle_impute_missing_data(self):
        """
        Testing impute_missing_data() with NaN as a middle value (not the first or last value).
        """
        df1 = pd.DataFrame({'Time': [0, 1, 2], 'Vals': [10, np.nan, 20]})
        df2 = pd.DataFrame({'Time': [0, 1, 2], 'Vals': [10.0, 15.0, 20.0]})

        assert impute_missing_data(df1).equals(df2)

    def test_NaN_only_impute_missing_data(self):
        """
        Testing impute_missing_data() with NaN as only value.
        """
        df1 = pd.DataFrame({'Time': [0], 'Vals': [np.nan]})
        df2 = pd.DataFrame({'Time': [0], 'Vals': [0]})

        assert impute_missing_data(df1).equals(df2)

    def test_no_NaN_impute_missing_data(self):
        """
        Testing impute_missing_data() with no NaN.
        """
        df1 = pd.DataFrame({'Time': [0], 'Vals': [22]})
        df2 = pd.DataFrame({'Time': [0], 'Vals': [22]})

        assert impute_missing_data(df1).equals(df2)


#########################
# IMPUTE_OUTLIERS() TESTS
#########################
class Test_impute_outliers:
    def test_outlier_first_impute_outliers(self):
        """
        Testing impute_outliers() with outlier as first value.
        """
        df1 = pd.DataFrame({'Time': [0, 1, 2, 3, 4, 5], 'Daily Top': ["GME", "AMC", "BB", "DOGE", "NOK", "BTC"],
                            'Vals': [420, 17.8, 15, 1, 25, 17]})
        df2 = pd.DataFrame({'Time': [0, 1, 2, 3, 4, 5], 'Daily Top': ["GME", "AMC", "BB", "DOGE", "NOK", "BTC"],
                            'Vals': [16.4, 17.8, 15, 1, 25, 17]})

        assert impute_outliers(df1).equals(df2)

    def test_outlier_last_impute_outliers(self):
        """
        Testing impute_outliers() with outlier as last value.
        """
        df1 = pd.DataFrame({'Time': [0, 1, 2, 3, 4, 5], 'Daily Top': ["GME", "AMC", "BB", "DOGE", "NOK", "BTC"],
                            'Vals': [5, 17.8, 15, 1, 25, 420]})
        df2 = pd.DataFrame({'Time': [0, 1, 2, 3, 4, 5], 'Daily Top': ["GME", "AMC", "BB", "DOGE", "NOK", "BTC"],
                            'Vals': [5, 17.8, 15, 1, 25, 13]})

        assert impute_outliers(df1).equals(df2)

    def test_outlier_middle_impute_outliers(self):
        """
        Testing impute_outliers() outlier as a middle value (not the first or last value).
        """
        df1 = pd.DataFrame({'Time': [0, 1, 2, 3, 4, 5], 'Daily Top': ["GME", "AMC", "BB", "DOGE", "NOK", "BTC"],
                            'Vals': [5, 17.8, 15, 420, 25, 1]})
        df2 = pd.DataFrame({'Time': [0, 1, 2, 3, 4, 5], 'Daily Top': ["GME", "AMC", "BB", "DOGE", "NOK", "BTC"],
                            'Vals': [5, 17.8, 15, 20, 25, 1]})

        assert impute_outliers(df1).equals(df2)

    def test_no_outlier_impute_outliers(self):
        """
        Testing impute_outliers() with no oulier.
        """
        df1 = pd.DataFrame({'Time': [0, 1, 2, 3, 4, 5], 'Daily Top': ["GME", "AMC", "BB", "DOGE", "NOK", "BTC"],
                            'Vals': [5, 17.8, 15, 16, 25, 1]})
        df2 = pd.DataFrame({'Time': [0, 1, 2, 3, 4, 5], 'Daily Top': ["GME", "AMC", "BB", "DOGE", "NOK", "BTC"],
                            'Vals': [5, 17.8, 15, 16, 25, 1]})

        assert impute_outliers(df1).equals(df2)

    def test_multiple_outlier_impute_outliers(self):
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
class Test_longest_continuous_run:
    def test_longest_continuous_run(self):
        """
        Testing longest_continuous_run().
        """
        df1 = pd.DataFrame({'Time': [0, 1, 2, 3, 4, 5, 6, 7, 8, 9],
                            'Daily Top': ["GME", "AMC", "BB", "DOGE", "NOK", "BTC", "NIO", "DIS", "ETH", "JD"],
                            'Vals': [10, 17.8, 15, np.nan, 25, 17, 18, 19, 500, 700]})
        df2 = pd.DataFrame({'Time': [4, 5, 6, 7, 8, 9],
                            'Daily Top': ["NOK", "BTC", "NIO", "DIS", "ETH", "JD"],
                            'Vals': [25.0, 17.0, 18.0, 19.0, 500.0, 700.0]})

        df3 = pd.DataFrame({'Time': [0, 1, 2, 3, 4, 5, 6, 7, 8, 9],
                            'Daily Top': ["GME", "AMC", "BB", "DOGE", "NOK", "BTC", "NIO", "DIS", "ETH", "JD"],
                            'Vals': [np.nan, 17.8, 15, 16, 25, 17, 18, 19, 500, 700]})
        df4 = pd.DataFrame({'Time': [1, 2, 3, 4, 5, 6, 7, 8, 9],
                            'Daily Top': ["AMC", "BB", "DOGE", "NOK", "BTC", "NIO", "DIS", "ETH", "JD"],
                            'Vals': [17.8, 15.0, 16.0, 25.0, 17.0, 18.0, 19.0, 500.0, 700.0]})
        # print(longest_continuous_run(df1))
        assert longest_continuous_run(df1).equals(df2)
        assert longest_continuous_run(df3).equals(df4)

    def test_no_NaN_longest_continuous_run(self):
        """
        Testing longest_continuous_run() with no NaN values.
        """
        df1 = pd.DataFrame({'Time': [0, 1, 2, 3, 4, 5, 6, 7, 8, 9],
                            'Daily Top': ["GME", "AMC", "BB", "DOGE", "NOK", "BTC", "NIO", "DIS", "ETH", "JD"],
                            'Vals': [10, 17.8, 15, 18, 25, 17, 18, 19, 500, 700]})
        df2 = pd.DataFrame({'Time': [0, 1, 2, 3, 4, 5, 6, 7, 8, 9],
                            'Daily Top': ["GME", "AMC", "BB", "DOGE", "NOK", "BTC", "NIO", "DIS", "ETH", "JD"],
                            'Vals': [10, 17.8, 15, 18, 25, 17, 18, 19, 500, 700]})

        assert longest_continuous_run(df1).equals(df2)

    def test_all_NaN_longest_continuous_run(self):
        """
        Testing longest_continuous_run() with all NaN values.
        """
        df1 = pd.DataFrame({'Time': [0, 1, 2, 3, 4],
                            'Daily Top': ["GME", "AMC", "BB", "DOGE", "NOK"],
                            'Vals': [np.nan, np.nan, np.nan, np.nan, np.nan]})
        df2 = pd.DataFrame({'Time': [],
                            'Daily Top': [],
                            'Vals': []})

        assert longest_continuous_run(df1).equals(df2)


###############
# CLIP() TESTS
###############
class Test_clip:
    def test_clip(self):
        """
        Testing clip().
        """
        df1 = pd.DataFrame({'Time': [0, 1, 2, 3, 4],
                            'Daily Top': ["GME", "AMC", "BB", "DOGE", "NOK"],
                            'Vals': [10, 12, 45, 88, 90]})
        df2 = pd.DataFrame({'Time': [1, 2, 3],
                            'Daily Top': ["AMC", "BB", "DOGE"],
                            'Vals': [12, 45, 88]})

        # df3 = pd.DataFrame({'Time': ["1/1", "1/2", "1/3", "1/4", "1/5"],
        #                     'Daily Top': ["GME", "AMC", "BB", "DOGE", "NOK"],
        #                     'Vals': [10, 12, 45, 88, 90]})
        # df4 = pd.DataFrame({'Time': ["1/3", "1/4", "1/5"],
        #                     'Daily Top': ["BB", "DOGE", "NOK"],
        #                     'Vals': [45, 88, 90]})

        assert clip(df1, 1.0, 3.0).equals(df2)
        # assert clip(df3, '1/3', '1/5').equals(df4)

    def test_end_less_than_start_clip(self):
        """
        Testing clip() where end_time is less than start_time.
        """
        df1 = pd.DataFrame({'Time': [0, 1, 2, 3, 4],
                            'Daily Top': ["GME", "AMC", "BB", "DOGE", "NOK"],
                            'Vals': [10, 12, 45, 88, 90]})
        df2 = pd.DataFrame({'Time': [2, 3, 4],
                            'Daily Top': ["BB", "DOGE", "NOK"],
                            'Vals': [45, 88, 90]})

        assert clip(df1, 2, 1).equals(df2)

    def test_invalid_times_clip(self):
        """
        Testing clip() where end_time and/or start_time is invalid.
        """
        df1 = pd.DataFrame({'Time': [0, 1, 2, 3, 4],
                            'Daily Top': ["GME", "AMC", "BB", "DOGE", "NOK"],
                            'Vals': [10, 12, 45, 88, 90]})
        df2 = pd.DataFrame({'Time': [],
                            'Daily Top': [],
                            'Vals': []})

        df3 = pd.DataFrame({'Time': [0, 1, 2, 3, 4],
                            'Daily Top': ["GME", "AMC", "BB", "DOGE", "NOK"],
                            'Vals': [10, 12, 45, 88, 90]})
        df4 = pd.DataFrame({'Time': [3, 4],
                            'Daily Top': ["DOGE", "NOK"],
                            'Vals': [88, 90]})

        assert clip(df1, 5, 8).equals(df2)
        assert clip(df3, 3, 6).equals(df4)

    def test_equal_times_clip(self):
        """
        Testing clip() where end_time and start_time are equal.
        """
        df1 = pd.DataFrame({'Time': [0, 1, 2, 3, 4],
                            'Daily Top': ["GME", "AMC", "BB", "DOGE", "NOK"],
                            'Vals': [10, 12, 45, 88, 90]})
        df2 = pd.DataFrame({'Time': [1],
                            'Daily Top': ["AMC"],
                            'Vals': [12]})

        assert clip(df1, 1, 1).equals(df2)


#####################
# ASSIGN_TIME() TESTS
#####################
class Test_assign_time:
    def test_assign_time(self):
        """
        Testing assign_time().
        """
        df1 = pd.DataFrame({'Daily Top': ["GME", "AMC", "BB", "DOGE", "NOK"],
                            'Vals': [10, 12, 45, 88, 90]})
        df2 = pd.DataFrame({'Times': [1.0, 2.0, 3.0, 4.0, 5.0],
                            'Daily Top': ["GME", "AMC", "BB", "DOGE", "NOK"],
                            'Vals': [10, 12, 45, 88, 90]})

        df3 = pd.DataFrame({'Daily Top': ["GME", "AMC", "BB", "DOGE", "NOK"],
                            'Vals': [10, 12, 45, 88, 90]})
        df4 = pd.DataFrame({'Times': [0.0, 5.0, 10.0, 15.0, 20.0],
                            'Daily Top': ["GME", "AMC", "BB", "DOGE", "NOK"],
                            'Vals': [10, 12, 45, 88, 90]})

        assert assign_time(df1, 1.0, 1.0).equals(df2)
        assert assign_time(df3, 0.0, 5.0).equals(df4)

    def test_decreasing_assign_time(self):
        """
        Testing assign_time() with a negative start and increment arguments.
        """
        df1 = pd.DataFrame({'Daily Top': ["GME", "AMC", "BB", "DOGE", "NOK"],
                            'Vals': [10, 12, 45, 88, 90]})
        df2 = pd.DataFrame({'Times': [0, -1, -2, -3, -4],
                            'Daily Top': ["GME", "AMC", "BB", "DOGE", "NOK"],
                            'Vals': [10, 12, 45, 88, 90]})

        df3 = pd.DataFrame({'Daily Top': ["GME", "AMC", "BB", "DOGE", "NOK"],
                            'Vals': [10, 12, 45, 88, 90]})
        df4 = pd.DataFrame({'Times': [-5, -10, -15, -20, -25],
                            'Daily Top': ["GME", "AMC", "BB", "DOGE", "NOK"],
                            'Vals': [10, 12, 45, 88, 90]})

        assert assign_time(df1, 0, -1).equals(df2)
        assert assign_time(df3, -5, -5).equals(df4)


###################
# DIFFERENCE()
###################
class Test_difference:
    def test_general_difference(self):
    	"""
    	Test general use case of the difference function.
    	"""
    	test_input = {
    		"Times": [0, 1, 2, 3, 4, 5],
    		"Values": [1, 0, 9, 10, 8, 4]
    	}
    	df_test_input = pd.DataFrame(test_input)
    	test_output = {
    		"Times": [0, 1, 2, 3, 4],
    		"Values": [1, 9, 1, 2, 4]
    	}
    	df_test_output = pd.DataFrame(test_output)
    	df_actual_output = difference(df_test_input)
    	assert list(df_actual_output.iloc[:, -1]) == list(df_test_output.iloc[:, -1])

    def test_negatives_difference(self):
    	"""
    	Test use case of the difference function with negatives.
    	"""
    	test_input = {
    		"Times": [0, 1, 2, 3, 4, 5],
    		"Values": [-1, 0, -9, 10, 8, -4]
    	}
    	df_test_input = pd.DataFrame(test_input)
    	test_output = {
    		"Times": [0, 1, 2, 3, 4],
    		"Values": [1, 9, 19, 2, 12]
    	}
    	df_test_output = pd.DataFrame(test_output)
    	df_actual_output = difference(df_test_input)
    	assert list(df_actual_output.iloc[:, -1]) == list(df_test_output.iloc[:, -1])

    def test_empty_difference(self):
    	"""
    	Test use case of the difference function where there are no entries.
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
    	df_actual_output = difference(df_test_input)
    	assert list(df_actual_output.iloc[:, -1]) == list(df_test_output.iloc[:, -1])

    def test_one_entry_difference(self):
    	"""
    	Test the use case of the difference function where there are entries (one entry),
    	but it's not enough to calculate a difference.
    	"""
    	test_input = {
    		"Times": [0],
    		"Values": [1]
    	}
    	df_test_input = pd.DataFrame(test_input)
    	test_output = {
    		"Times": [],
    		"Values": []
    	}
    	df_test_output = pd.DataFrame(test_output)
    	df_actual_output = difference(df_test_input)
    	assert list(df_actual_output.iloc[:, -1]) == list(df_test_output.iloc[:, -1])

    def test_two_entry_difference(self):
    	"""
    	Test the use case of the difference function where there are just enough
    	entries to calculate a difference (2 entries).
    	"""
    	test_input = {
    		"Times": [0, 1],
    		"Values": [1, 5]
    	}
    	df_test_input = pd.DataFrame(test_input)
    	test_output = {
    		"Times": [0],
    		"Values": [4]
    	}
    	df_test_output = pd.DataFrame(test_output)
    	df_actual_output = difference(df_test_input)
    	assert list(df_actual_output.iloc[:, -1]) == list(df_test_output.iloc[:, -1])

    def test_monocolumn_difference(self):
    	"""
    	Test mono-column use case of the difference function.
    	"""
    	test_input = {
    		"Values": [1, 0, 9, 10, 8, 4]
    	}
    	df_test_input = pd.DataFrame(test_input)
    	test_output = {
    		"Values": [1, 9, 1, 2, 4]
    	}
    	df_test_output = pd.DataFrame(test_output)
    	df_actual_output = difference(df_test_input)
    	assert list(df_actual_output.iloc[:, -1]) == list(df_test_output.iloc[:, -1])

    def test_multicolumn_difference(self):
    	"""
    	Test multi-column use case of the difference function.
    	"""
    	test_input = {
    		"Months": [0, 1, 2, 3, 4, 5],
    		"Days": [12, 1, 6, 24, 20, 18],
    		"Values": [1, 0, 9, 10, 8, 4]
    	}
    	df_test_input = pd.DataFrame(test_input)
    	test_output = {
    		"Months": [0, 1, 2, 3, 4],
    		"Days": [12, 1, 6, 24, 20],
    		"Values": [1, 9, 1, 2, 4]
    	}
    	df_test_output = pd.DataFrame(test_output)
    	df_actual_output = difference(df_test_input)
    	assert list(df_actual_output.iloc[:, -1]) == list(df_test_output.iloc[:, -1])


##################
# SCALING() TESTS
##################
class Test_scaling:
    def test_general_scaling(self):
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

    def test_negative_scaling(self):
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

    def test_same_scaling(self):
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

    def test_min_scaling(self):
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

    def test_empty_scaling(self):
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

    def test_monocolumn_scaling(self):
    	"""
    	Test case where only one column is provided
    	"""
    	test_input = [1, 0, 9, 10, 8, 4]
    	df_test_input = pd.DataFrame(test_input)
    	test_output = [0.1, 0, .9, 1, .8, .4]
    	df_test_output = pd.DataFrame(test_output)
    	df_actual_output = scaling(df_test_input)
    	assert list(df_actual_output.iloc[:, -1]) == list(df_test_output.iloc[:, -1])

    def test_multicolumn_scaling(self):
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
class Test_standardize:
    def test_general_standardize(self):
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

    def test_negative_standardize(self):
    	"""
    	Test the negative use case of the standardize function
    	"""
    	test_input = {
    		"Times": [0, 1, 2, 3, 4, 5],
    		"Values": [-1, 0, -9, -10, -8, -4]
    	}
    	df_test_input = pd.DataFrame(test_input)
    	input_mean = df_test_input.iloc[:, -1].mean()
    	input_std = df_test_input.iloc[:, -1].std()
    	test_output = {
    		"Times": [0, 1, 2, 3, 4, 5],
    		"Values": [
    			(-1 - input_mean) / input_std,
    			(0 - input_mean) / input_std,
    			(-9 - input_mean) / input_std,
    			(-10 - input_mean) / input_std,
    			(-8 - input_mean) / input_std,
    			(-4 - input_mean) / input_std
    		]
    	}
    	df_test_output = pd.DataFrame(test_output)
    	df_actual_output = standardize(df_test_input)
    	assert list(df_actual_output.iloc[:, -1]) == list(df_test_output.iloc[:, -1])

    def test_empty_standardize(self):
    	"""
    	Test the empty time series use case of the standardize function
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
    	df_actual_output = standardize(df_test_input)
    	assert list(df_actual_output.iloc[:, -1]) == list(df_test_output.iloc[:, -1])

    def test_zerodiv_standardize(self):
    	"""
    	Test the edge case of the standardize function when variation is 0
    	"""
    	test_input = {
    		"Times": [0, 1, 2],
    		"Values": [5, 5, 5]
    	}
    	df_test_input = pd.DataFrame(test_input)
    	input_mean = df_test_input.iloc[:, -1].mean()
    	input_std = df_test_input.iloc[:, -1].std()
    	test_output = {
    		"Times": [0, 1, 2],
    		"Values": [0, 0, 0]
    	}
    	df_test_output = pd.DataFrame(test_output)
    	print(df_test_output)
    	df_actual_output = standardize(df_test_input)
    	print(df_actual_output)
    	assert list(df_actual_output.iloc[:, -1]) == list(df_test_output.iloc[:, -1])

    def test_monocolumn_standardize(self):
    	"""
    	Test case where only one column is provided
    	"""
    	test_input = {
    		"Values": [1, 0, 9, 10, 8, 4]
    	}
    	df_test_input = pd.DataFrame(test_input)
    	input_mean = df_test_input.iloc[:, -1].mean()
    	input_std = df_test_input.iloc[:, -1].std()
    	test_output = {
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

    def test_multicolumn_standardize(self):
    	"""
    	Test the use case where a multiple of columns are provided
    	"""
    	test_input = {
    		"Months": [0, 1, 2, 3, 4, 5],
    		"Days": [12, 1, 6, 24, 20, 18],
    		"Values": [1, 0, 9, 10, 8, 4]
    	}
    	df_test_input = pd.DataFrame(test_input)
    	input_mean = df_test_input.iloc[:, -1].mean()
    	input_std = df_test_input.iloc[:, -1].std()
    	test_output = {
    		"Months": [0, 1, 2, 3, 4, 5],
    		"Days": [12, 1, 6, 24, 20, 18],
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
class Test_logarithm:
    def test_logarithm(self):
    	"""
    	Tests 1 column dataframe
    	"""
    	ts = pd.DataFrame({
    		"Times": [0, 1, 2, 3, 4, 5],
    		"Values": [1.0, 0.0, 9.0, 10.0, 8.0, 4.0]
    	})

    	logarithm(ts)

    def test_logarithm(self):
        """
        Tests 1 column dataframe
        """
        ts = pd.DataFrame({
            "Times": [0, 1, 2, 3, 4, 5],
            "Values": [1.0, 0.0, 9.0, 10.0, 8.0, 4.0]
        })

        logarithm(ts)

    def test_log10_2(self):

        ts2 = pd.DataFrame({

            'Time': [0, 1, 2, 3, 4, 5, 6],
            'Daily Top': ["GME", "AMC", "BB", "DOGE", "NOK", "BTC", "ETH"],
            'Vals': [10, 12, 45, 88, 90, 77, 81]
        })
        df = logarithm(ts2)


##########################
# CUBIC ROOT TESTS
##########################
class Test_cubic_root:
    def test_cubic_root(self):

    	ts = pd.DataFrame({
    		"Times": [0, 1, 2, 3, 4, 5],
    		"Values": [1.0, 0.0, 9.0, 10.0, 8.0, 4.0]
    	})

    	df = cubic_root(ts)

    def test_cubic_root2(self):

        ts2 = pd.DataFrame({

            'Time': [0, 1, 2, 3, 4, 5, 6],
            'Daily Top': ["GME", "AMC", "BB", "DOGE", "NOK", "BTC", "ETH"],
            'Vals': [10, 12, 45, 88, 90, 77, 81]
        })
        df = cubic_root(ts2)


##########################
# SPLIT_DATA() TESTS
##########################
class Test_split_data:
    def test_split_data(self):
    	ts = pd.DataFrame({
    		"greetings": ["hello", "hello1", "hello2", "hello3", "hello4", "hello5"],
    		"date": ["monday", "tue", "wed", "thu", "friday", "saturday"],
    		"Values": [1.0, 0.0, 9.0, 10.0, 8.0, 4.0]
    	})
    	

    	val1 = .25
    	val2 = .50
    	val3 = .25
    	#ts = logarithm(ts)
    	ts = cubic_root(ts)
    	res = split_data(ts, val1, val2, val3)



    def test_split_data2(self):
        
        ts2 = pd.DataFrame({
            "Values": [1.0, 0.0, 9.0, 10.0, 8.0, 4.0]
        })

        val1 = .25
        val2 = .50
        val3 = .25
        #ts = logarithm(ts)
        ts2 = cubic_root(ts2)
        res = split_data(ts2, val1, val2, val3)
        print(res)




#######################
# DESIGN_MATRIX() TESTS
#######################
class Test_design_matrix:
    def test_design_matrix(self):
        """
        Testing design_matrix().
        """
        df1 = pd.DataFrame({'Time': [0, 1, 2, 3, 4, 5, 6],
                            'Daily Top': ["GME", "AMC", "BB", "DOGE", "NOK", "BTC", "ETH"],
                            'Vals': [10, 12, 45, 88, 90, 77, 81]})
        ret1 = ((np.array([[10, 12], [12, 45], [45, 88], [88, 90]]),
                      np.array([[45, 88], [88, 90], [90, 77], [77, 81]])))

        op1 = design_matrix(df1, 2.0, 2.0)
        in1_vs_op1 = op1[0] == ret1[0]
        in1 = in1_vs_op1.all()
        out1_vs_op1 = op1[1] == ret1[1]
        out1 = out1_vs_op1.all()
        assert in1 and out1

    def test_again_design_matrix(self):
        """
        Testing design_matrix() again.
        """
        df1 = pd.DataFrame({'Time': [0, 1, 2, 3, 4, 5, 6],
                            'Daily Top': ["GME", "AMC", "BB", "DOGE", "NOK", "BTC", "ETH"],
                            'Vals': [10, 12, 45, 88, 90, 77, 81]})
        ret1 = (np.array([[10, 12, 45], [12, 45, 88], [45, 88, 90]]),
                      np.array([[88, 90], [90, 77], [77, 81]]))

        op1 = design_matrix(df1, 3.0, 2.0)
        in1_vs_op1 = op1[0] == ret1[0]
        in1 = in1_vs_op1.all()
        out1_vs_op1 = op1[1] == ret1[1]
        out1 = out1_vs_op1.all()
        assert in1 and out1

##########################
# DENOISE TESTS
##########################
class test_denoise:
    def test_split_general(self):
        ts1 = pd.DataFrame({
            "greetings": ["hello", "hello1", "hello2", "hello3", "hello4", "hello5", "hello", "hello1", "hello2", "hello3", "hello4", "hello5"],
            "date": ["monday", "tue", "wed", "thu", "friday", "saturday", "monday", "tue", "wed", "thu", "friday", "saturday"],
            "Values": [1.0, 0.0, 9.0, 10.0, 8.0, 4.0, 1.0, 0.0, 9.0, 10.0, 8.0, 4.0]
        })
        

    def test_denoise_general2(self):
        
        ts2 = pd.DataFrame({ "Values": [1.0, 0.0, 9.0, 10.0, 8.0, 4.0, 5.0, 5.5, 6.0, 5.5, 6.0] })


    def test_denoise_general2(self):
       
        ts3 = pd.DataFrame({"greetings": ["hello2", "hello3", "hello4", "hello5", "hello", "hello1", "hello2", "hello3", "hello4", "hello5"],
                                "date": ["wed", "thu", "friday", "saturday", "monday", "tue", "wed", "thu", "friday", "saturday"],
                                "Values": [3.333333, 6.333333, 9.000000, 7.333333, 4.333333, 1.666667, 3.333333, 6.333333, 9.000000, 7.333333]
        })


def mse_test():
    ts2 = pd.DataFrame({ "Values": [1.0, 0.0, 9.0, 10.0, 8.0, 4.0, 5.0, 5.5, 6.0, 5.5, 6.0] })
    x = ts2

    for item in x:
        print(item)

#############
# DB2TS()
#############
class Test_db2ts:
    def test_general_db2ts(self):
    	"""
    	Tests general use case of db2ts()
    	"""
    	test_input = [
    			[1, 2, 3],
    			[2, 3, 4],
    			[3, 4, 5]
    		]
    	db_test_input = np.array(test_input)
    	test_output = pd.DataFrame([1, 2, 3, 4, 5])
    	df_test_output = pd.DataFrame(test_output)
    	df_actual_output = db2ts(db_test_input)
    	assert list(df_actual_output.iloc[:, -1]) == list(df_test_output.iloc[:, -1])

    def test_negatives_db2ts(self):
    	"""
    	Tests use case of db2ts() with negative numbers
    	"""
    	test_input = [
    			[1, -2, 2],
    			[-2, 2, 4],
    			[2, 4, -5],
    			[4, -5, -1]
    		]
    	db_test_input = np.array(test_input)
    	test_output = pd.DataFrame([1, -2, 2, 4, -5, -1])
    	df_test_output = pd.DataFrame(test_output)
    	df_actual_output = db2ts(db_test_input)
    	assert list(df_actual_output.iloc[:, -1]) == list(df_test_output.iloc[:, -1])

    def test_empty_db2ts(self):
    	"""
    	Tests use case of db2ts() with no provided data
    	"""
    	test_input = []
    	db_test_input = np.array(test_input)
    	test_output = pd.DataFrame([])
    	df_test_output = pd.DataFrame(test_output)
    	df_actual_output = db2ts(db_test_input)
    	assert df_test_output.equals(df_actual_output)

    def test_empty_row_db2ts(self):
    	"""
    	Tests use case of db2ts() with only an empty row
    	"""
    	test_input = [[]]
    	db_test_input = np.array(test_input)
    	test_output = pd.DataFrame([])
    	df_test_output = pd.DataFrame(test_output)
    	df_actual_output = db2ts(db_test_input)
    	assert df_test_output.equals(df_actual_output)

    def test_single_row_db2ts(self):
    	"""
    	Tests use case of db2ts() with only one row
    	"""
    	test_input = [[1, 2, 3, 4]]
    	db_test_input = np.array(test_input)
    	test_output = pd.DataFrame([1, 2, 3, 4])
    	df_test_output = pd.DataFrame(test_output)
    	df_actual_output = db2ts(db_test_input)
    	assert df_test_output.equals(df_actual_output)

    def test_single_col_db2ts(self):
    	"""
    	Tests use case of db2ts() with only one column
    	"""
    	test_input = [[1], [2], [3], [4]]
    	db_test_input = np.array(test_input)
    	test_output = pd.DataFrame([1, 2, 3, 4])
    	df_test_output = pd.DataFrame(test_output)
    	df_actual_output = db2ts(db_test_input)
    	assert df_test_output.equals(df_actual_output)
