Authors -

  * Cameron Jordal
  * JT Kashuba
  * Noah Kruss
  * Nick Titzler
  * River Veek

Group - Keyboard Warriors

Last Modified - 2/8/2021


# CIS 422 - Project 1

## System Description:

This system is a code library that provides functionality for processing time
series data - specifically cleaning it up, displaying different forms of output,
and producing / applying forecasting models, all in the form of a data processing tree.
The Time Series Tree stores references of the operations that the data will be processed
through upon a tree or path execution command. Each path through the tree is
called a “pipeline”.  

## How To Install and Run

See Installation_Instructions.txt

## Software Dependencies

See Requirements.txt

Python 3.0 or later

## REPO Organization

* tree.py - Time-Series Tree class and functions
* file_io.py - Functions for opening and saving Time Series data
* modeling.py - Functions for creating a forecasting model
* preprocessing.py - Functions for cleaning and scaling Time Series data
* visualiztion.py - Functions for plotting Time Series data and computing error
on forecasting models.
* testing - A suite of test files that contain test cases for each python file
listed above.
* timeSeriesData - A directory of different Time Series data which was used as
examples in the creation of this project.
