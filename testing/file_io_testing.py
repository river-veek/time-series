"""
Tests for time_series.py containing the time series class

Author: Nick Titzler

"""
import numpy as np
import sys
sys.path.append("../")
import time_series as TS
import file_io as fio



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


	


def main():
	#test1_timeSeriesData1()
	test2_timeSeriesData2()
	pass





main()