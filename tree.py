"""
Tree class for product library

Author: Noah Kruss
"""

"""
!!!!! Need to still check if new node conflicts with previous
"""


########################
# IMPORTS AND GLOBALS
########################
from anytree import Node, RenderTree, NodeMixin
import os
import shutil

import preprocessing as pre_proc
import visualization as vis
import modeling as mod

########################
# Valid operations for nodes
########################
pre_processing = {"denoise": (pre_proc.denoise, None),
                  "impute_missing_data": (pre_proc.impute_missing_data, None),
                  "impute_outliers": (pre_proc.impute_outliers, None),
                  "longest_continuous_run": (pre_proc.longest_continuous_run, None),
                  "clip": (pre_proc.clip, [0,1]),
                  "assign_time": (pre_proc.assign_time, [0,2]),
                  "difference": (pre_proc.difference, None),
                  "scaling": (pre_proc.scaling, None),
                  "standardize": (pre_proc.standardize, None),
                  "logarithm": (pre_proc.logarithm, None),
                  "cubic_root": (pre_proc.cubic_root, None),
                  "split_data": (pre_proc.split_data, [3,4,5]),
                  "design_matrix": (pre_proc.design_matrix, [0,1]),
                  "ts2db": (mod.ts2db, [6,3,4,5,0,1,7]),
                  "mlp_model": (mod.mlp_model, [0,2,8])
                  }

visualization = {"plot": (vis.plot, None),
                 "histogram": (vis.histogram, None),
                 "box_plot": (vis.box_plot, None),
                 "normality_test": (vis.normality_test, None),
                 "mse": (vis.mse, [6]),
                 "mape": (vis.mape, [6]),
                 "smape": (vis.smape, [6])
                 }


########################
# validate input functions
########################
def validate_operation(operation: str):
    """
    Function to validate that an operation is valid

    Calls:
        None
    Call By:
        tree.
        tree.

    Return - Bool
    """
    valid = False

    if function in pre_processing.keys():
        valid = True
    elif function in visualization.keys():
        valid = True

    return valid

def validate_inputs(data_start,
                    data_end,
                    increment,
                    perc_training,
                    perc_valid,
                    perc_test,
                    input_filename,
                    output_filename,
                    layers):
    """
    Function to validate that an inputs for operations are valid types

    Calls:
        None
    Call By:
        tree.
        tree.

    Return - Bool
    """
    valid = True

    if type(data_start) != float:
        print("Invalid Input - data_start={data_start} is not a float")
        valid = False
    elif type(data_end) != float:
        print("Invalid Input - data_end={data_end} is not a float")
        valid = False
    elif type(increment) != float:
        print("Invalid Input - increment={increment} is not a float")
        valid = False
    elif type(perc_training) != float:
        print("Invalid Input - perc_training={perc_training} is not a float")
        valid = False
    elif type(perc_valid) != float:
        print("Invalid Input - perc_valid={perc_valid} is not a float")
        valid = False
    elif type(perc_test) != float:
        print("Invalid Input - increment={perc_test} is not a float")
        valid = False
    elif type(input_filename) != str:
        print("Invalid Input - input_filename={input_filename} is not a str")
        valid = False
    elif type(output_filename) != str:
        print("Invalid Input - output_filename={output_filename} is not a str")
        valid = False
    elif type(layers) != tuple:
        print("Invalid Input - layers={layers} is not a tuple")
        valid = False

    return valid

########################
# node class
########################
class Operation_node(NodeMixin):
    """
    Operation_node is a node class for a Tree built off of the basic
    anytree node class. Operation_node class includes aditionaly functionality
    for storing function calls and node depth then NodeMixin
    """

    def __init__(self,
                 name: str,
                 function: str,
                 parent = None,
                 data_start = None,
                 data_end = None,
                 increment = None,
                 perc_training = None,
                 perc_valid = None,
                 perc_test = None,
                 input_filename = None,
                 output_filename = None,
                 layers = None):
        """
        Initilize node properties: (name, depth, parent, child_list)
            name is a string in the form - 'operation_call-node_index'
            parent is a Operation_node (can be None) that is the parent
            child_list is an empty list to store child nodes
        """

        super(Operation_node, self).__init__()
        self.name = name
        self.parent = parent
        self.child_list = []
        self.is_a_leaf = True

        if function in pre_processing.keys():
            self.function = pre_processing[key]
        elif function in visualization.keys():
            self.function = visualization[key]

        self.function_inputs = [data_start,
                                data_end,
                                increment,
                                perc_training,
                                perc_valid,
                                perc_test,
                                input_filename,
                                output_filename,
                                layers]

    def add_child(self, new_node: 'Operation_node'):
        """
        Function to add a child node to the childe_list

        Calls:
            None
        Call By:
            Tree.add_node(operation, parent_index)

        Returns - None
        """

        self.child_list.append(new_node)
        self.is_a_leaf = False

    def change_operation(self,
                         new_operation: str
                         data_start = None,
                         data_end = None,
                         increment = None,
                         perc_training = None,
                         perc_valid = None,
                         perc_test = None,
                         input_filename = None,
                         output_filename = None,
                         layers = None):
        """
        Function to replace the operation string of the node with (new_operation)

        Calls:
            None
        Call By:
            Tree.replace_node(new_operation, node_index)

        Returns - None
        """
        #pull out node index
        node_index = self.name.split('-')[1]

        #create new node name string
        new_name = f"{new_operation}-{node_index}"
        self.name = new_name

        #update function inputs
        self.function_inputs = [data_start,
                                data_end,
                                increment,
                                perc_training,
                                perc_valid,
                                perc_test,
                                input_filename,
                                output_filename,
                                layers]

    def get_decendents(self):
        """
        Function to get and return a list of the nodes decendents

        Calls:
            Operation_node.get_decendents()
        Call By:
            copy_subtree(main_tree, node_index)
            Operation_node.get_decendents()

        Returns - str
        """
        decendent_list = []

        for child in self.child_list:
            decendent_list.append(child)
            decendent_list += child.get_decendents()

        return decendent_list

class TS_Tree:

    def __init__(self):
        """
        Initilize a Tree with a denoise root node
        """
        #make denoise root node and place it in the Tree
        root_node = Operation_node("denoise-0", 0, None)
        self.nodes = [root_node]

    def print_tree(self):
        """
        Function for displaying a string repersentation of the tree

        Calls:
            RenderTree()
        Call By:
            User_interface.py - main()

        Returns - None
        """
        for pre, fill, node in RenderTree(self.nodes[0]):
            print("%s%s" % (pre, node.name))

    def add_node(self,
                 operation: str,
                 parent_index: int,
                 data_start = None,
                 data_end = None,
                 increment = None,
                 perc_training = None,
                 perc_valid = None,
                 perc_test = None,
                 input_filename = None,
                 output_filename = None,
                 layers = None):
        """
        Function for adding a new node to the tree. Takes a operation string and
        the index of the parent (parent_index). New node gets added as a child
        of the parent and added into the list of tree nodes.

        Calls:
            tree.py - Operation_node.__init__()
            tree.py - Operation_node.add_child()
        Call By:
            tree.py - add_subtree()

        Returns - None
        """
        #check to make sure parent_index is valid
        if parent_index > len(tree.nodes) or parent_index < 0:
            print(f"Invalid parent_index - {parent_index}")
            valid = False
        #check to make sure operation is valid
        if validate_operation(operation):
            print(f"Invalid operation - {operation}")
            return None
        # check to make sure function inputs are valid
        if validate_inputs(data_start,
                           data_end,
                           increment,
                           perc_training,
                           perc_valid,
                           perc_test,
                           input_filename,
                           output_filename,
                           layers) == False:
            return None

        #get the parent node based off of the parent index
        parent_node = self.nodes[parent_index]

        #check new operation doesn't conflict with parents
        parent_operation = parent_node.name.split("-")[0]
        # if ____

        #set up name for the new node depending of the given operation and the
        ## number of nodes currently in the tree
        new_node_name = f"{operation}-{len(self.nodes)}"

        #create and add new node to the tree
        new_node = Operation_node(new_node_name,
                                  parent_node,
                                  data_start = data_start,
                                  data_end = data_end,
                                  increment = increment,
                                  prec_training = perc_training,
                                  perc_valid = perc_valid,
                                  perc_test = perc_test,
                                  input_filename = input_filename,
                                  output_filename = output_filename,
                                  layers = layers)

        parent_node.add_child(new_node)

        self.nodes.append(new_node)

    def replace_node(self,
                     new_operation: str,
                     node_index: int,
                     data_start = None,
                     data_end = None,
                     increment = None,
                     perc_training = None,
                     perc_valid = None,
                     perc_test = None,
                     input_filename = None,
                     output_filename = None,
                     layers = None):
        """
        Function to replace the operation with (new_operation) of the
        (node_index) node within the tree

        Calls:
            tree.py - Operation_node.change_operation()
        Call By:
            User_interface.py - main()

        Returns - None
        """
        #check to make sure node_index is valid
        if node_index > len(self.nodes) or node_index < 0:
            print("Invalid node_index")
            return None
        #check to make sure operation is valid
        if validate_operation(new_operation):
            print(f"Invalid operation - {new_operation}")
            return None
        # check to make sure function inputs are valid
        if validate_inputs(data_start,
                           data_end,
                           increment,
                           perc_training,
                           perc_valid,
                           perc_test,
                           input_filename,
                           output_filename,
                           layers) == False:
            return None

        node = self.nodes[node_index]
        node.change_operation(new_operation,
                              data_start = data_start,
                              data_end = data_end,
                              increment = increment,
                              prec_training = perc_training,
                              perc_valid = perc_valid,
                              perc_test = perc_test,
                              input_filename = input_filename,
                              output_filename = output_filename,
                              layers = layers)

    def get_path(self, node_index: int):
        """
        Function to get a list of the pipeline leading to the node at (node_index)

        Calls:
            tree.py - Operation_node.change_operation(new_operation)
        Call By:
            tree.py - TS_Tree.execute_path()

        Returns - List
        """
        #check to make sure node_index is valid
        if node_index > len(self.nodes) or node_index < 0:
            print("Invalid node_index")
            return None

        #assemble the piepline of nodes from the bottom up
        pipeline = []
        node = self.nodes[node_index]
        while(node != None):
            pipeline.append(node)
            node = node.parent

        #revese pipeline to get in into the correct order
        pipeline.reverse()

        return pipeline

    def execute_path(self, time_series, node_index: int):
        """
        Function for running the pipeline from the root to a node with
        (node_index) within a tree on the given time series (time_series)

        Calls:
            tree.py - TS_Tree.get_peth()
        Call By:
            tree.py - TS_Tree.execute_tree()

        Returns - None
        """
        #check to make sure node_index is valid
        if node_index > len(self.nodes) or node_index < 0:
            print("Invalid node_index")
            return None

        pipeline = self.get_path(node_index)

        for node in pipeline:

            #get fucntion reference
            func = node.function[0]
            #get the function input lists
            func_inputs = node.function_inputs

            #condition where function only takes a time series
            if node.function[1] == None:
                time_series = func(time_series)
            #function with aditional inputs
            else:
                #get a list of the inputs for nodes function operation
                inputs = []
                for index in node.function[1]:
                    inputs.append(func_inputs[index])

                #make function call with apropriate input parameters
                num_inputs = len(inputs)
                if num_inputs == 1:
                    time_series = func(time_series, inputs[0])
                elif num_inputs == 2:
                    time_series = func(time_series, inputs[0], inputs[1])
                elif num_inputs == 3:
                    time_series = func(time_series, inputs[0], inputs[1], inputs[2])
                elif num_inputs == 4:
                    time_series = func(time_series, inputs[0], inputs[1], inputs[2], inputs[3])
                elif num_inputs == 5:
                    time_series = func(time_series, inputs[0], inputs[1], inputs[2], inputs[3], inputs[5])

    def execute_tree(self, time_series):
        """
        Function for running every possible pipeline from the root to a leaf
        within a tree on the given time series (time_series)

        Calls:
            tree.py - TS_Tree.execute_path()
        Call By:

        Returns - None
        """

        #loop through each node in the tree
        for node in self.nodes:
            #if node is a leaf execute the pipeline from it to the root
            if node.is_a_leaf:
                index = node.name.split("-")[1]
                self.execute_path(time_series, index)


#------------------------------------------------------------------------------

#created functions that deal with the Tree class
def copy_subtree(main_tree: TS_Tree, node_index: int):
    """
    Takes a Tree and returns a copy of the subtree starting at node (node_index)
    in a save file named (save_file_name) in the TreeFiles folder.

    Calls:
        tree.py - save_tree()
    Call By:

    Returns - Tree
    """
    sub_tree = TS_Tree()

    new_root = main_tree.nodes[node_index]
    new_root.parent = None

    #get list of nodes that will make up the subtree
    node_list = new_root.get_decendents()

    #set up sub_tree
    sub_tree.nodes[0] = new_root

    sub_tree.nodes += node_list

    return sub_tree

def add_subtree(tree: TS_Tree, node_index: int, subtree: TS_Tree):
    """
    Function to add (subtree) TS_Tree to be a child of the target node given by
    (node_index) of (tree).

    Calls:
        None
    Call By:
        None

    Returns - None
    """
    #check to make sure node_index is valid
    if node_index > len(self.nodes) or node_index < 0:
        print("Invalid node_index")
        return None

    index_offset = len(tree.nodes)

    for i in range(len(subtree.nodes)):
        node = subtree.nodes[i]
        node_info = node.name.split("-")
        node_operation = node_info[0]
        node_index = int(node_info[1])

        function_inputs = node.function_in

        if i == 0:
            tree.add_node(node_operation,
                          node_index,
                          data_start = data_start,
                          data_end = data_end,
                          increment = increment,
                          prec_training = perc_training,
                          perc_valid = perc_valid,
                          perc_test = perc_test,
                          input_filename = input_filename,
                          output_filename = output_filename,
                          layers = layers)
        else:
            parent_info = node.parent.name.split("-")
            parent_index = int(node_info[1])

            tree.add_node(node_operation,
                          parent_index + index_offset,
                          data_start = data_start,
                          data_end = data_end,
                          increment = increment,
                          prec_training = perc_training,
                          perc_valid = perc_valid,
                          perc_test = perc_test,
                          input_filename = input_filename,
                          output_filename = output_filename,
                          layers = layers)


def save_tree(tree: TS_Tree, save_file_name: str):
    """
    Function to save target tree (tree) stucture into a file named (save_file_name).
    The resulting save_file will save each node on a line as follows
        'node.name,parent.name'

    Calls:
        None
    Call By:
        User_interface.py - main()

    Returns - None
    """

    if tree == None:
        print(f"\nError saving - No Tree Inputed\n")
        return None

    node_list = tree.nodes

    #open file to write the tree data to
    save_file = open(save_file_name, "w")

    for node in node_list:
        #case for root node
        if node.parent == None:
            save_file.write(f"{node.name},None,")
        else:
            save_file.write(f"{node.name},{node.parent.name},")
        save_file.write(f"{node.function_inputs[0]},")
        save_file.write(f"{node.function_inputs[1]},")
        save_file.write(f"{node.function_inputs[2]},")
        save_file.write(f"{node.function_inputs[3]},")
        save_file.write(f"{node.function_inputs[4]},")
        save_file.write(f"{node.function_inputs[5]},")
        save_file.write(f"{node.function_inputs[6]},")
        save_file.write(f"{node.function_inputs[7]},")
        save_file.write(f"{node.function_inputs[8]}\n")

    save_file.close()

def load_tree(save_file_name: str):
    """
    Function to load tree stucture from given file (save_file_name).

    Calls:
        None
    Call By:
        User_interface.py - main()

    Return - TS_Tree
    """

    # #open file to write the tree data file
    # try:
    #     path_to_file = os.getcwd()+ "/TreeFiles/" + save_file_name
    #     load_file = open(path_to_file, "r")
    # except:
    #     print(f"\nError loading {save_file_name} - Not Found\n")
    #     return None

    try:
        loaded_tree = TS_Tree(save_file_name)

        Lines = load_file.readlines()
        for line in Lines:
            line = line.strip().split(',')

            node_info = line[0].split('-')
            node_operation = node_info[0]
            node_index = node_info[1]

            #get the function parameters
            if node_info[2] == "None":
                data_start = None
            else
                data_start = float(node_info[2])

            if node_info[3] == "None":
                data_end = None
            else:
                data_end= float(node_info[3])

            if node_info[4] == "None":
                increment = None
            else:
                increment = float(node_info[4])

            if node_info[5] == "None":
                perc_training = None
            else:
                perc_training = float(node_info[5])

            if node_info[6] == "None":
                perc_valid = None
            else:
                perc_valid = float(node_info[6])

            if node_info[7] == "None":
                perc_test = None
            else:
                perc_test = float(node_info[7])

            if node_info[8] == "None":
                input_filename = None
            else:
                input_filename = node_info[8]

            if node_info[9] == "None":
                output_filename = None
            else:
                output_filename = node_info[9]

            if node_info[10] == "None":
                layers = None
            else:
                layers = node_info[10]

            #Add node to tree
            #root node condition
            if node_index == '0':
                loaded_tree.nodes[0].change_operation(node_operation)
                func_inputs = [data_start,
                               data_end,
                               increment,
                               perc_training,
                               perc_valid,
                               perc_test,
                               input_filename,
                               output_filename,
                               layers]
                loaded_tree.nodes[0].function_inputs = func_inputs
            else:
                parent_info = line[1].split('-')
                parent_index = int(parent_info[1])
                loaded_tree.add_node(node_operation,
                                     parent_index,
                                     data_start = data_start,
                                     data_end = data_end,
                                     increment = increment,
                                     prec_training = perc_training,
                                     perc_valid = perc_valid,
                                     perc_test = perc_test,
                                     input_filename = input_filename,
                                     output_filename = output_filename,
                                     layers = layers)

        load_file.close()
    except:
        print(f"\nError loading {save_file_name} - Bad Format\n")
        return None

    return loaded_tree
