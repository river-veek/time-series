from tree import *

tree = TS_Tree()

tree.add_node("denoise", 0, increment=7.0)
tree.add_node("impute_outliers", 1)

tree.add_node("plot", 2)

tree.add_node("design_matrix", 2, data_start = 20.0, data_end = 10.0)
tree.add_node("mlp_model", 4, layers=[100,])
tree.add_node("mlp_forecast", 5)

tree.print_tree()

#processed = tree.execute_path("timeSeriesData/TimeSeriesData1/1_temperature_test.csv", 3)
forecast = tree.execute_path("timeSeriesData/TimeSeriesData1/1_temperature_test.csv", 5)
