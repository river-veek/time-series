"""
----------------------------------------------------------------------------------------
Tests for time_series.py containing the time series class

Author - Nick Titzler
Group - Keyboard Warriors
Last Modified - 2/9/21
----------------------------------------------------------------------------------------
"""

import numpy as np
import sys
sys.path.append("../")
import file_io as fio
import pandas as pd
import visualization as plot
import matplotlib.pyplot as plt
import preprocessing as pre


"""
###############################
	READ_FROM_FILE TESTS
###############################
"""

def test1_timeSeriesData1():
	"""
	test time series creation from timeSeriesData1 files

	"""
	fileNames = ["1_temperature_test.csv","1_temperature_train.csv","2_temperature_subsampled_test.csv",
	"2_temperature_subsampled_train.csv", "3_passengers_test.csv","3_passengers_train.csv","4_irradiance_test.csv",
	"4_irradiance_train.csv", "5_irradiance_subsampled_test.csv", "5_irradiance_subsampled_train.csv", "6_sunspots_test.csv", "6_sunspots_train.csv",
	"7_distribution_subsampled_norm_test.csv", "7_distribution_subsampled_norm_train.csv", "8_distribution_subsampled_test.csv", "8_distribution_subsampled_train.csv"]

	fname = "../timeSeriesData/TimeSeriesData1/1_temperature_test.csv"

	try:
		for item in fileNames:
			fname = "../timeSeriesData/TimeSeriesData1/"+item

			ts = fio.read_from_file(fname)
	except:
		print("error in test 1")



def test2_timeSeriesData2():

	fname1 = "../timeSeriesData/TimeSeriesData1/1_temperature_test.csv"
	fname2 = "../timeSeriesData/TimeSeriesData2/wind_aristeomercado_10m_complete.csv"
	fname3 = "../timeSeriesData/TimeSeriesData2/wind_aristeomercado_10m_complete.csv"

	ts = fio.read_from_file(fname1)
	ts2 = fio.read_from_file(fname2)
	#plot.plot([ts, ts2])



	#plot.histogram([ts, ts2])


	#plot.box_plot(ts)
	#plot.box_plot([ts, ts2])

	#plot.plot(ts)

def test_plot():
	fname1 = "../timeSeriesData/TimeSeriesData1/1_temperature_test.csv"
	fname2 = "../timeSeriesData/TimeSeriesData2/wind_aristeomercado_10m_complete.csv"
	fname3 = "../timeSeriesData/TimeSeriesData1/3_passengers_train.csv"


	ts = fio.read_from_file(fname1)
	ts2 = fio.read_from_file(fname2)
	ts3 = fio.read_from_file(fname3)

	print(ts)

	#plot.plot(ts3)
	plot.plot(ts)

def test_histogram():
	fname1 = "../timeSeriesData/TimeSeriesData1/1_temperature_test.csv"
	fname2 = "../timeSeriesData/TimeSeriesData2/wind_aristeomercado_10m_complete.csv"
	fname3 = "../timeSeriesData/TimeSeriesData1/3_passengers_train.csv"

	ts = fio.read_from_file(fname1)
	ts2 = fio.read_from_file(fname2)

	#plot.histogram([ts, ts2])
	#plot.histogram(ts2)
	plot.histogram(ts2)

def test_normality():

	fname1 = "../timeSeriesData/TimeSeriesData1/1_temperature_test.csv"
	ts = fio.read_from_file(fname1)

	plot.normality_test(ts)

def test_box():
	fname1 = "../timeSeriesData/TimeSeriesData1/1_temperature_test.csv"
	fname2 = "../timeSeriesData/TimeSeriesData2/wind_aristeomercado_10m_complete.csv"
	fname3 = "../timeSeriesData/TimeSeriesData1/3_passengers_train.csv"

	ts = fio.read_from_file(fname1)
	ts2 = fio.read_from_file(fname2)
	ts3 = fio.read_from_file(fname3)



	plot.box_plot(ts3)



def main():
	#test_plot()
	#test_box()
	#test_histogram()
	#test_plot()



	return 1





main()
