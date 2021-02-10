"""
----------------------------------------------------------------------------------------
Tests for tree.py containing the the TS_Tree class

Author - Noah Kruss
Group - Keyboard Warriors
Last Modified - 2/9/2021
----------------------------------------------------------------------------------------
"""

"""
todo
    write input chack for operations to makes sure a end operation doesn't get followed
"""

import sys
sys.path.append("../")
from tree import *
import file_io as fio
import pandas as pd

def test_create_tree():
    print("\n##Test basic Tree Creation##")
    test_tree = TS_Tree()
    test_tree.print_tree()

    return test_tree

def test_add_node(test_tree):

    print("\n##Test Adding Nodes to Tree##")

    #check invaid node_index
    print("\n#testing invalid node_index#")
    test_tree.add_node("denoise", 7)

    #check invaid operation
    print("\n#testing invalid operation#")
    test_tree.add_node("in-valid", 0)

    #check invaid function inputs
    print("\n#testing invalid function input#")
    test_tree.add_node("clip", 0, data_start=1.0, data_end="2.0")
    test_tree.add_node("clip", 0, data_start=1, data_end=2.0)
    test_tree.add_node("clip", 0, input_filename=1)

    #build basic tree
    print("\n#building tree#")
    test_tree.add_node("denoise", 0)
    test_tree.add_node("clip", 0, data_start=1.0, data_end=2.0)
    test_tree.print_tree()

    test_tree.add_node("impute_missing_data", 1)
    test_tree.add_node("longest_continuous_run", 1)
    test_tree.add_node("plot", 4)
    test_tree.add_node("histogram", 4)
    test_tree.add_node("mse", 5, input_filename="test_file.txt")
    test_tree.add_node("mlp_model", 2, layers=[0.0,1.0,2.0,3.0])
    test_tree.print_tree()

    #check invaid function inputs
    print("\n#testing adding node to parent that has to be a leaf#")
    test_tree.add_node("denoise", 7)

    test_tree.print_tree()

    return test_tree

def test_replace_operation(test_tree):

    print("\n##Test Replacing Nodes Operation in Tree##")

    #check invaid node_index
    print("\n#testing invalid node_index#")
    test_tree.replace_node("denoise", 9)

    #check invaid operation
    print("\n#testing invalid operation#")
    test_tree.replace_node("in-valid", 0)

    print("\n#testing replacing non-leaf node operation with a lead operation#")
    test_tree.replace_node("mse", 2)

    print("\n#testing replacing node with bad inputs#")
    test_tree.add_node("clip", 2, output_filename="test_file.txt")

    #build basic tree
    print("\n#replacing node operation tree#")
    test_tree.replace_node("impute_outliers", 4)
    test_tree.replace_node("difference", 1)
    test_tree.print_tree()

    return test_tree

def test_copy_add_subtree(test_tree):
    print("\n##Test Copying SubTree##")
    sub_tree = copy_subtree(test_tree, 4)
    sub_tree.print_tree()
    test_tree.print_tree()

    print("\n##Test Adding SubTree##")
    add_subtree(test_tree, 3, sub_tree)
    test_tree.print_tree()

def test_copy_path(test_tree):
    print("\n##Test Copying Path##")
    path_copy = copy_path(test_tree, 5)
    path_copy.print_tree()

def test_save_load_tree(test_tree):

    print("\n##Test saving and loading Tree##")
    save_tree(test_tree, "tree_test.txt")
    loaded_tree = load_tree("tree_test.txt")

    print("\n#Saved Tree#")
    test_tree.print_tree()
    print("\n#Loaded Tree#")
    loaded_tree.print_tree()
    save_tree(loaded_tree, "tree_test_loaded.txt")

def test_execute_pipeline(test_tree):
    tree = TS_Tree()
    tree.replace_node("longest_continuous_run", 0)
    tree.add_node("impute_missing_data", 0)
    tree.add_node("assign_time", 1, data_start=1.0, increment=.2)
    tree.add_node("plot", 2)
    #tree.add_node("clip", 2, data_start=1.0, data_end=10.0)

    print("\n##Test executting a pipeline to node 3##")
    tree.print_tree()
    fname1 = "../timeSeriesData/TimeSeriesData2/AtmPres2005NovMin.csv"
    ts = fio.read_from_file(fname1)
    results = tree.execute_path(ts, 3)

    tree2 = TS_Tree()
    tree2.replace_node("read_from_file", 0, input_filename="../timeSeriesData/TimeSeriesData2/AtmPres2005NovMin.csv")


def test_execute_tree():
    pass

def main():

    test_tree = test_create_tree()

    test_tree = test_add_node(test_tree)

    test_tree = test_replace_operation(test_tree)

    test_save_load_tree(test_tree)

    test_copy_add_subtree(test_tree)

    test_copy_path(test_tree)

    test_execute_pipeline(test_tree)


main()
