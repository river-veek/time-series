from tree import *

tree = TS_Tree()

tree.add_node("denoise", 0, increment=7.0)
tree.add_node("impute_outliers", 1)
tree.add_node("standardize", 2)

tree.add_node("histogram", 3)
tree.add_node("normality_test", 3)

tree.add_node("design_matrix", 3, data_start = 20.0, data_end = 10.0)
tree.add_node("mlp_model", 6, layers=[100,])
tree.add_node("mlp_forecast", 7, input_filename="timeSeriesData/TimeSeriesData1/1_temperature_db_test.csv")

tree.add_node("db2ts", 8)
tree.add_node("write_to_file", 9, output_filename="1_temperature_test_futures.csv")

tree.add_node("mse", 8, input_filename="timeSeriesData/TimeSeriesData1/1_temperature_test.csv")
tree.add_node("mape", 8, input_filename="timeSeriesData/TimeSeriesData1/1_temperature_test.csv")
tree.add_node("smape", 8, input_filename="timeSeriesData/TimeSeriesData1/1_temperature_test.csv")

tree.print_tree()

#processed = tree.execute_path("timeSeriesData/TimeSeriesData1/1_temperature_test.csv", 3)
#normality = tree.execute_path("timeSeriesData/TimeSeriesData1/1_temperature_train.csv", 5)
#print(normality)
tree.execute_tree("timeSeriesData/TimeSeriesData1/1_temperature_train.csv")
