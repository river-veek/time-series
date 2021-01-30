"""
Tests for tree.py containing the the TS_Tree class

Author: Noah Kruss

"""

"""
todo
    write input chack for operations to makes sure a end operation doesn't get followed
"""
import sys
sys.path.append("../")
from tree import *

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
    test_tree.add_node("impute_missing_data", 1)
    test_tree.add_node("longest_continuous_run", 1)
    test_tree.add_node("plot", 4)
    test_tree.add_node("histogram", 4)
    test_tree.add_node("mse", 5, input_filename="test_file.txt")
    test_tree.print_tree()

    #check invaid function inputs
    print("\n#testing adding node to parent that has to be a leaf#")
    test_tree.add_node("denoise", 7)

    test_tree.print_tree()

    return test_tree

def test_replace_operation(test_tree):

    print("\n##Test Replacing Nodes Operation in Tree##")

    #check invaid node_index
    print("#testing invalid node_index#")
    test_tree.replace_node("denoise", 9)

    #check invaid operation
    print("#testing invalid operation#")
    test_tree.replace_node("in-valid", 0)

    print("\n#testing replacing non-leaf node operation with a lead operation#")
    test_tree.replace_node("mse", 2)

    #build basic tree
    print("#replacing node operation tree#")
    test_tree.replace_node("input_outliers", 4)
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

def test_copy_path():
    pass

def test_combine_trees():
    pass

def test_save_load_tree(test_tree):

    print("\n##Test saving and loading Tree##")
    save_tree(test_tree, "tree_test.txt")
    loaded_tree = load_tree("tree_test.txt")

    print("\n#Saved Tree#")
    test_tree.print_tree()
    print("\n#Loaded Tree#")
    loaded_tree.print_tree()

def test_load_pipeline():
    pass

def test_save_pipeline():
    pass

def test_execute_pipeline():
    pass

def test_execute_tree():
    pass




def main():

    test_tree = test_create_tree()
    test_tree = test_add_node(test_tree)
    test_tree = test_replace_operation(test_tree)

    test_save_load_tree(test_tree)
    test_copy_add_subtree(test_tree)

    # test_add_node(test_tree)
    #
    # #test replacing a node operation
    # test_tree.replace_node("replaced", 5)
    # test_tree.print_tree()
    #
    # save_tree(test_tree, "save_file.txt")
    #
    # loaded_tree = load_tree("save_file.txt")
    # print("Loaded Tree:")
    # loaded_tree.print_tree()
    #
    # print("Sub-Tree:")
    # sub_tree = copy_subtree(test_tree, 1)
    # sub_tree.print_tree()

main()
