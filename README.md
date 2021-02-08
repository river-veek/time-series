--------------------------------------------------------------------------------
Author - Noah Kruss
Group - Keyboard Warriors
Last Modified - 2/8/2021
--------------------------------------------------------------------------------

# System Description:

This system is a code library that provides functionality for processing time
series data - specifically cleaning it up, displaying different forms of output,
and producing / applying forecasting models, all in the form of a data processing tree.
The Time Series Tree stores references of the operations that the data will be processed
through upon a tree or path execution command. Each path through the tree is
called a “pipeline”.  

# How To Install

See Installation_Instructions.txt

# REPO Organization

* tree.py - Time-Series Tree class and functions
* file_io.py - Functions for opening and saving Time Series data
* modeling.py - Functions for creating a forecasting model 
* preprocessing.py - Functions for cleaning and scaling Time Series data
* visualiztion.py - Functions for plotting Time Series data and computing error
on forecasting models.
