Authors -

  * Cameron Jordal
  * JT Kashuba
  * Noah Kruss
  * Nick Titzler
  * River Veek

Group - Keyboard Warriors

Last Modified - 2/9/2021


# CIS 422 - Project 1
# Time Series Manipulations, Modeling, and Forecasting

## System Description:

This system is a code library that provides functionality for processing time
series data - specifically cleaning it up, displaying different forms of output,
and producing / applying forecasting models, all in the form of a data
processing tree. The Time Series Tree (TS_Tree) stores references of these
operations and the data is processed after calling a path / tree execution
command. Paths in the tree can also be referred to as “pipelines”.  

## How To Install and Run

See Installation_Instructions.txt for a step-by-step install guide

## Software Dependencies

Python 3.0 or later

See requirements.txt for a full list of dependencies


## REPO Organization

* tree.py - Time-Series Tree class and functions
* file_io.py - Functions for opening and saving Time Series data files
* modeling.py - Functions for creating forecasting models
* preprocessing.py - Functions for cleaning up and scaling Time Series data
* visualization.py - Functions for plotting Time Series data and computing
errors in forecasted models.
* testing - A suite of test case files for each of the python files listed above.
* timeSeriesData - A directory of different Time Series data files which were
used as examples in the creation of this project.
* documentation - A directory containing the following pieces of documentation
    * SRS.pdf - Software Requirements Specification
    * SDS.pdf - Software Design Specification
    * Project_Plan - A directory of PDF files containing the roles / responsibilities
of each team member, the individual progress made by each team member,
documentation from group meetings, agendas for team meetings, benchmarks / goals,
documentation specifications, and system requirements.
    * Programmer_Documentation.pdf -

# Some helpful examples at a glance:

## Tree node operations:

* `add_node(operation: str, node_index, input_parameters)`

* `replace_node(operation: str, node_index, input_parameters)`

* `add_subtree(TREE_1, node_index, subtree)`

* `copy_subtree(TREE_2, subtree_root_index)`

* `save_tree(“output_file.txt”)`

* `load_tree(“input_file.txt”)`

* `execute_path(“fileName.txt”, node_index)`

* `execute_tree(“fileName.txt”)`



## input_parameters for specific functions:

*Note: A `time series` gets called in each of these functions, but only by `execute_path` or `execute_tree`. The user will never actually pass a `time series` to these functions themselves as an argument. It will happen implicitly in all function calls when the user calls `execute_path` or `execute_tree`. To reiterate, `execute_path` and `execute_tree` are the only
two functions that require the user to use a `time series` as an argument.*

**These input_parameters MUST be declared, otherwise the user will get errors**

* `design_matrix(data_start = <float>, data_end = <float>)`

* `denoise(increment = <float>)`

* `impute_missing_data()`

* `impute_outliers()`

* `longest_continuous_run()`

* `clip(data_start = <float>, data_end = <float>)`

* `assign_time(data_start = <float>, increment = <float>)`

* `difference()`

* `scaling()`

* `standardize()`

* `logarithm()`

* `cubic_root()`

* `split_data(perc_training = <float>, perc_valid = <float>, perc_test = <float>)`

* `ts2db(input_filename = <str>, perc_training = <float>, perc_val = <float>, perc_test =
<float>)`

* `data_start = <float>, data_end = <float>, output_filename = <str>)`

* `db2ts()`

* `plot()`

* `histogram()`

* `box_plot()`

* `normality_test()`

* `mse(input_filename = <str>)`

* `mape(input_filename = <str>)`

* `smape(input_filename = <str>)`

* `mlp_model(layers = <list>)`

* `mlp_forecast(input_filename = <str>)`

* `read_from_file()`

* `write_to_file(output_filename = <str>)`
