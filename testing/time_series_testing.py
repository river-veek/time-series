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
import time_series as TS



def test1_mean():
	ts = TS.TimeSeries()
	ts.series = {"0":0,"1":1,"2":2,"3":3,"4":4,"5":5}
	print(ts.mean())
	assert(ts.mean() == np.mean([0,1,2,3,4,5]))


def test2_stdiv():
	ts = TS.TimeSeries()
	ts.series = {"0":0,"1":1,"2":2,"3":3,"4":4,"5":5}
	assert(ts.stddiv() == np.std([0,1,2,3,4,5]))


def main():
	test1_mean()
	test2_stdiv()


main()
