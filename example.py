from tree import *

tree = TS_Tree()

tree.add_node("denoise", 0, increment=7.0)
tree.add_node("impute_outliers", 1)

tree.add_node("plot", 2)

tree.add_node("design_matrix", 2, data_start = 20.0, data_end = 10.0)
tree.add_node("mlp_model", 4, layers=[100,])
tree.add_node("mlp_forecast", 5, input_filename="timeSeriesData/TimeSeriesData1/1_temperature_db_test.csv")

tree.add_node("db2ts", 6)
tree.add_node("write_to_file", 7, output_filename="timeSeriesData/TimeSeriesData1/1_temperature_test_futures.csv")

#tree.add_node("mse", 6, input_filename="timeSeriesData/TimeSeriesData1/1_temperature_test.csv")

tree.print_tree()

#processed = tree.execute_path("timeSeriesData/TimeSeriesData1/1_temperature_test.csv", 3)
forecast = tree.execute_path("timeSeriesData/TimeSeriesData1/1_temperature_train.csv", 8)
