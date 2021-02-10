"""
----------------------------------------------------------------------------------------
Tests for Tree File I/O

Author - Nick Titzler
Group - Keyboard Warriors
Last Modified - 1/29/21
----------------------------------------------------------------------------------------
"""
import numpy as np
import sys
sys.path.append("../")
import file_io as fio
import pandas as pd


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

	fname1 = "../timeSeriesData/TimeSeriesData2/AtmPres2005NovMin.csv"
	ts = fio.read_from_file(fname1)

	fname2 = "../timeSeriesData/TimeSeriesData2/wind_aristeomercado_10m_complete.csv"
	ts = fio.read_from_file(fname2)

	fname3 = "../timeSeriesData/TimeSeriesData1/9_distribution_subsampled_train_empty.csv"

	fname4 = "../timeSeriesData/TimeSeriesData1/AtmPres2005NovMinEmpty.csv"

	fname5 = "../timeSeriesData/TimeSeriesData1/save1.p"

	ts1 = fio.read_from_file(fname5)

	print(ts1)
	ts = fio.read_from_file(fname4)
	print(ts)

def test3_read_from_file_pandas():
	#df = pd.read_csv(r'../timeSeriesData/TimeSeriesData1/1_temperature_test.csv')
	#df = pd.read_csv('../timeSeriesData/TimeSeriesData2/AtmPres2005NovMin.csv')

	df = fio.read_from_file('../timeSeriesData/TimeSeriesData2/AtmPres2005NovMin.csv')


	print(df)
	#print(df)
	#print(d2)
	d3 = fio.read_from_file('../timeSeriesData/TimeSeriesData2/AtmPres2005NovMin.csv')

	print(df.iloc[:,-1:])
	#print(d3.iloc[:,-3])
	return 0

def test4_empty_file():

	df = fio.read_from_file('../timeSeriesData/TimeSeriesData1/oneItem.csv')
	print(df)
"""
###############################
	WRITE_TO_FILE TESTS
###############################

"""

def test1_write_to_file():
	ts = TS.TimeSeries()
	ts = fio.read_from_file("../timeSeriesData/TimeSeriesData1/1_temperature_test.csv")

	fio.write_to_file(ts, "1_temperature_test_output.csv")



def main():
	#test1_timeSeriesData1()
	#test2_timeSeriesData2()

	#test1_write_to_file()
	#test3_read_from_file_pandas()
	#test4_empty_file()

	return 1





main()
