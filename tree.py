"""
----------------------------------------------------------------------------------------
Tree class for product library

The TS_Tree object will store and organize nodes which contain function call
to be applied to time series data. A pipeline within the tree (a path from the
root node to the target node) can then be executed to apply the chain of
functions onto the time series data.

Author - Noah Kruss
Group - Keyboard Warriors
Last Modified - 2/9/21
----------------------------------------------------------------------------------------
"""


########################
# IMPORTS AND GLOBALS
########################
from anytree import Node, RenderTree, NodeMixin

import preprocessing as pre_proc
import visualization as vis
import modeling as mod
import file_io as fio

########################
# Valid operations for nodes
########################
pre_processing = {"denoise": (pre_proc.denoise, [2]),
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
                  "ts2db": (pre_proc.ts2db, [6,3,4,5,0,1,7]),
                  "db2ts": (pre_proc.db2ts, None),
                  "mlp_model": (mod.mlp_model, [12]),
                  "mlp_forecast": (mod.mlp_forecast, [6]),
                  "read_from_file": (fio.read_from_file, None),
                  "write_to_file": (fio.write_to_file, [7])
                  }

visualization = {"plot": (vis.plot, [7]),
                 "histogram": (vis.histogram, [7]),
                 "box_plot": (vis.box_plot, [7]),
                 "normality_test": (vis.normality_test, None),
                 "mse": (vis.mse, [6]),
                 "mape": (vis.mape, [6]),
                 "smape": (vis.smape, [6])
                 }

leaf_functions = ["split_data", "ts2db", "mse", "mape", "smape", "write_to_file"]

path_dependent = ["design_matrix","ts2db", "mlp_model"]

########################
# validate input functions
########################
def validate_operation(operation: str):
    """
    Function to validate that an operation is valid

    Calls:
        None
    Call By:
        tree.py - TS_Tree.add_node()
        tree.py - TS_Tree.replace_node()

    Return - Bool
    """
    valid = False

    if operation in pre_processing.keys():
        valid = True
    elif operation in visualization.keys():
        valid = True

    return valid

def validate_operation_order(operation: str, parent_operation: str):
    """
    Function to validate that the node ordering is valid

    Calls:
        None
    Call By:
        tree.py - TS_Tree.add_node()
        tree.py - TS_Tree.replace_node()

    Return - Bool
    """
    valid = True

    if parent_operation in leaf_functions:
        print(f"Error - parent function '{parent_operation}' can't have children")
        valid = False

    elif (parent_operation == "design_matrix" and operation != "mlp_model"):
        print(f"Error - design_matrix needs to be followed by mlp_model")
        valid = False

    elif (parent_operation == "mlp_model" and operation != "mlp_forecast"):
        print(f"Error - mlp_model needs to be followed by mlp_forecast")
        valid = False

    elif (parent_operation == "mlp_forecast" and operation != "mse") and \
         (parent_operation == "mlp_forecast" and operation != "mape") and \
         (parent_operation == "mlp_forecast" and operation != "smape") and \
         (parent_operation == "mlp_forecast" and operation != "db2ts"):
        print(f"Error - mlp_forecast needs to be followed by mse, mape, smape, or db2ts")
        valid = False

    elif (parent_operation == "db2ts" and operation != "write_to_file") and \
         (parent_operation == "mlp_forecast" and (operation not in visualization.keys())):
        print(f"Error - db2ts needs to be followed by write_to_file or visualiztion/error function")
        valid = False

    return valid

def validate_inputs(operation,
                    data_start,
                    data_end,
                    increment,
                    perc_training,
                    perc_valid,
                    perc_test,
                    input_filename,
                    output_filename,
                    m_i,
                    t_i,
                    m_0,
                    t_0,
                    layers):
    """
    Function to validate that an inputs for operations are valid types. If any
    of the inputs are invalid returns False

    Calls:
        None
    Call By:
        tree.py - TS_Tree.add_node()
        tree.py - TS_Tree.replace_node()

    Return - Bool
    """
    valid = True

    #go through each input and check that they are the valid type if not None
    if (type(data_start) != float) and (data_start != None):
        print(f"Invalid Input - data_start={data_start} is not a float")
        valid = False
    elif (type(data_end) != float) and (data_end != None):
        print(f"Invalid Input - data_end={data_end} is not a float")
        valid = False
    elif (type(increment) != float) and (increment != None):
        print(f"Invalid Input - increment={increment} is not a float")
        valid = False
    elif (type(perc_training) != float) and (perc_training != None):
        print(f"Invalid Input - perc_training={perc_training} is not a float")
        valid = False
    elif (type(perc_valid) != float) and (perc_valid != None):
        print(f"Invalid Input - perc_valid={perc_valid} is not a float")
        valid = False
    elif (type(perc_test) != float) and (perc_test != None):
        print(f"Invalid Input - perc_test={perc_test} is not a float")
        valid = False
    elif (type(input_filename) != str) and (input_filename != None):
        print(f"Invalid Input - input_filename={input_filename} is not a str")
        valid = False
    elif (type(output_filename) != str) and (output_filename != None):
        print(f"Invalid Input - output_filename={output_filename} is not a str")
        valid = False
    elif (type(layers) != list) and (layers != None):
        print(f"Invalid Input - layers={layers} is not a tuple")
        valid = False
    elif (type(m_i) != float) and (m_i != None):
        print(f"Invalid Input - m_i={m_i} is not a float")
        valid = False
    elif (type(t_i) != float) and (t_i != None):
        print(f"Invalid Input - t_i={t_i} is not a float")
        valid = False
    elif (type(m_0) != float) and (m_0 != None):
        print(f"Invalid Input - m_0={m_0} is not a float")
        valid = False
    elif (type(t_0) != float) and (t_0 != None):
        print(f"Invalid Input - t_0={m_0} is not a float")
        valid = False

    #check inputs match with the function
    if operation == "clip":
        if (data_start == None) or (data_end == None):
            print(f"Error - clip needs data_start and data_end")
            valid = False
    elif operation == "denoise":
        if (increment == None):
            print(f"Error - denoise needs data_start and data_end")
            valid = False
    elif operation == "assign_time":
        if (data_start == None) or (increment == None):
            print(f"Error - assign_time needs data_start and increment")
            valid = False
    elif operation == "split_data":
        if (perc_test == None) or (perc_valid == None) or (perc_training == None):
            print(f"Error - split_data needs perc_test, perc_valid, and perc_training")
            valid = False
    elif operation == "design_matrix":
        if (data_start == None) or (data_end == None):
            print(f"Error - design_matrix needs data_start and data_end")
            valid = False
    elif operation == "ts2db":
        if (input_filename == None) or (perc_test == None) or (perc_valid == None) or (perc_training == None) or (data_start == None) or (data_end == None) or (output_filename == None):
            print(f"Error - ts_2db needs input_filename, perc_test, perc_valid, perc_training, data_start, data_end, and output_filename")
            valid = False
    elif operation == "mlp_model":
        if (layers == None):
            print(f"Error - mlp_model needs layers")
            valid = False
    elif operation == "mlp_forecast":
        if (input_filename == None):
            print(f"Error - mlp_forecast needs input_filename")
            valid = False
    elif operation == "write_to_file":
        if (output_filename == None):
            print(f"Error - write_to_file needs output_filename")
            valid = False
    elif operation == "mse":
        if (input_filename == None):
            print(f"Error - mse needs input_filename")
            valid = False
    elif operation == "mape":
        if (input_filename == None):
            print(f"Error - mape needs input_filename")
            valid = False
    elif operation == "smape":
        if (input_filename == None):
            print(f"Error - smape needs input_filename")
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

    Function Inputs:
        data_start - float input that can be passed to functions (clip,
                     assign_time, design_matrix, ts2db, mlp_model)

        data_end - float input that can be passed to functions (clip,
                   design_matrix)

        increment - float input that can be passed to functions (assign_time,
                    mlp_model)

        perc_training - float input that can be passed to functions
                        (split_data, ts2db)

        perc_valid - float input that can be passed to functions
                     (split_data, ts2db)

        perc_test - float input that can be passed to functions
                    (split_data, ts2db)

        input_filename - str input that can be passed to functions (ts2db,
                         mse, mape, smape)

        output_filename - str input that can be passed to functions (ts2db)

        m_i - float input that can be passed to (design_matrix_2)

        t_i - float input that can be passed to (design_matrix_2)

        m_0 - float input that can be passed to (design_matrix_2)

        t_0 - float input that can be passed to (design_matrix_2)

        layers - list input that can be passed to (mlp_model)
    """

    def __init__(self,
                 name: str,
                 function: str,
                 parent,
                 data_start = None,
                 data_end = None,
                 increment = None,
                 perc_training = None,
                 perc_valid = None,
                 perc_test = None,
                 input_filename = None,
                 output_filename = None,
                 m_i = None,
                 t_i = None,
                 m_0 = None,
                 t_0 = None,
                 layers = None):
        """
        Initialize node properties:
            name - str in the form 'operation_call-node_index'

            function - str representation of function call

            parent - Operation_node (can be None) that is the parent of the node


        """

        super(Operation_node, self).__init__()
        self.name = name
        self.parent = parent
        self.child_list = []
        self.is_a_leaf = True

        if function in pre_processing.keys():
            self.function = pre_processing[function]
        elif function in visualization.keys():
            self.function = visualization[function]

        self.function_inputs = [data_start,
                                data_end,
                                increment,
                                perc_training,
                                perc_valid,
                                perc_test,
                                input_filename,
                                output_filename,
                                m_i,
                                t_i,
                                m_0,
                                t_0,
                                layers]

    def add_child(self, new_node: 'Operation_node'):
        """
        Function to add a child node to the child_list

        Calls:
            None
        Call By:
            Tree.add_node(operation, parent_index)

        Returns - None
        """

        self.child_list.append(new_node)
        self.is_a_leaf = False

    def change_operation(self,
                         new_operation: str,
                         data_start = None,
                         data_end = None,
                         increment = None,
                         perc_training = None,
                         perc_valid = None,
                         perc_test = None,
                         input_filename = None,
                         output_filename = None,
                         m_i = None,
                         t_i = None,
                         m_0 = None,
                         t_0 = None,
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

        #update function call
        if new_operation in pre_processing.keys():
            self.function = pre_processing[new_operation]
        elif new_operation in visualization.keys():
            self.function = visualization[new_operation]

        #update function inputs
        self.function_inputs = [data_start,
                                data_end,
                                increment,
                                perc_training,
                                perc_valid,
                                perc_test,
                                input_filename,
                                output_filename,
                                m_i,
                                t_i,
                                m_0,
                                t_0,
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

    def copy_node(self):
        """
        Function to return a duplicate of current node

        Calls:
            None
        Call By:
            tree.py - copy_path()
            tree.py - copy_subtree()

        Returns - Operation_node
        """
        #set up root node
        new_node = Operation_node("", "", None)
        new_node.name = self.name
        new_node.child_list = self.child_list
        new_node.parent = self.parent
        new_node.is_a_leaf = self.is_a_leaf
        new_node.function = self.function
        new_node.function_inputs = self.function_inputs

        return new_node


class TS_Tree:

    def __init__(self):
        """
        Initialize a Tree with a read_from_file root node
        """
        #make denoise root node and place it in the Tree
        root_node = Operation_node("read_from_file-0", "read_from_file", None)
        self.nodes = [root_node]

    def print_tree(self):
        """
        Function for displaying a string repersentation of the tree

        Calls:
            RenderTree()
        Call By:

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
                 m_i = None,
                 t_i = None,
                 m_0 = None,
                 t_0 = None,
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
        if parent_index >= len(self.nodes) or parent_index < 0:
            print(f"Invalid parent_index - {parent_index}")
            return None

        #check to make sure operation is valid
        if validate_operation(operation) == False:
            print(f"Invalid operation - {operation}")
            return None

        # check to make sure function inputs are valid
        if validate_inputs(operation,
                           data_start,
                           data_end,
                           increment,
                           perc_training,
                           perc_valid,
                           perc_test,
                           input_filename,
                           output_filename,
                           m_i,
                           t_i,
                           m_0,
                           t_0,
                           layers) == False:
            return None

        #get the parent node based off of the parent index
        parent_node = self.nodes[parent_index]

        #check new operation doesn't conflict with parents
        parent_operation = parent_node.name.split("-")[0]
        if validate_operation_order(operation, parent_operation) == False:
            return None

        #set up name for the new node depending of the given operation and the
        ## number of nodes currently in the tree
        new_node_name = f"{operation}-{len(self.nodes)}"

        #create and add new node to the tree
        new_node = Operation_node(new_node_name,
                                  operation,
                                  parent_node,
                                  data_start = data_start,
                                  data_end = data_end,
                                  increment = increment,
                                  perc_training = perc_training,
                                  perc_valid = perc_valid,
                                  perc_test = perc_test,
                                  input_filename = input_filename,
                                  output_filename = output_filename,
                                  m_i = m_i,
                                  t_i = t_i,
                                  m_0 = m_0,
                                  t_0 = t_0,
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
                     m_i = None,
                     t_i = None,
                     m_0 = None,
                     t_0 = None,
                     layers = None):
        """
        Function to replace the operation with (new_operation) of the
        (node_index) node within the tree

        Calls:
            tree.py - Operation_node.change_operation()
        Call By:

        Returns - None
        """
        #check to make sure node_index is valid
        if node_index >= len(self.nodes) or node_index < 0:
            print("Invalid node_index")
            return None

        node = self.nodes[node_index]
        parent_node = node.parent
        if parent_node != None:
            parent_operation = parent_node.name.split("-")[0]
        else:
            parent_operation = None

        #check to make sure operation is valid
        if validate_operation(new_operation) == False:
            print(f"Invalid operation - {new_operation}")
            return None
        if (new_operation in leaf_functions) and (node.is_a_leaf == False):
            print(f"Invalid operation - '{new_operation}' has to be a leaf")
            return None
        if validate_operation_order(new_operation, parent_operation) == False:
            return None
        if (node.is_a_leaf == False and new_operation in path_dependent):
            print(f"Invalid operation - '{new_operation}' is path dependent")
            return None


        # check to make sure function inputs are valid
        if validate_inputs(new_operation,
                           data_start,
                           data_end,
                           increment,
                           perc_training,
                           perc_valid,
                           perc_test,
                           input_filename,
                           output_filename,
                           m_i,
                           t_i,
                           m_0,
                           t_0,
                           layers) == False:
            return None

        node.change_operation(new_operation,
                              data_start = data_start,
                              data_end = data_end,
                              increment = increment,
                              perc_training = perc_training,
                              perc_valid = perc_valid,
                              perc_test = perc_test,
                              input_filename = input_filename,
                              output_filename = output_filename,
                              m_i = m_i,
                              t_i = t_i,
                              m_0 = m_0,
                              t_0 = t_0,
                              layers = layers)

    def get_path(self, node_index: int):
        """
        Function to get a list nodes of the pipeline leading to the node at
        (node_index) in the tree

        Calls:
            tree.py - Operation_node.change_operation(new_operation)
        Call By:
            tree.py - TS_Tree.execute_path()
            tree.py - copy_path()

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

    def execute_path(self, data_input, node_index: int):
        """
        Function for running the pipeline from the root to a node with
        (node_index) within a tree on the given data_input (time series or
        file_name of time series)

        Calls:
            tree.py - TS_Tree.get_peth()
        Call By:
            tree.py - TS_Tree.execute_tree()

        Returns - Time Series
        """
        #check to make sure node_index is valid
        if node_index >= len(self.nodes) or node_index < 0:
            print("Invalid node_index")
            return None

        pipeline = self.get_path(node_index)

        for node in pipeline:

            print(f"\n ###executing - {node.name}###")

            #get fucntion reference
            func = node.function[0]
            #get the function input lists
            func_inputs = node.function_inputs

            #condition where function only takes a time series
            if node.function[1] == None:
                data_input = func(data_input)

            #function with aditional inputs
            else:
                #get a list of the inputs for nodes function operation
                inputs = []
                for index in node.function[1]:
                    inputs.append(func_inputs[index])

                #make function call with apropriate input parameters
                num_inputs = len(inputs)
                if num_inputs == 1:
                    data_input = func(data_input, inputs[0])
                elif num_inputs == 2:
                    data_input = func(data_input, inputs[0], inputs[1])
                elif num_inputs == 3:
                    data_input = func(data_input, inputs[0], inputs[1], inputs[2])
                elif num_inputs == 4:
                    data_input = func(data_input, inputs[0], inputs[1], inputs[2], inputs[3])
                elif num_inputs == 5:
                    data_input = func(data_input, inputs[0], inputs[1], inputs[2], inputs[3], inputs[5])

        return data_input

    def execute_tree(self, data_input):
        """
        Function for running every possible pipeline from the root to a leaf
        within a tree on the given an data_input (time series or
        file_name of time series)

        Calls:
            tree.py - TS_Tree.execute_path()
        Call By:

        Returns - Dictonary of results of pipelines
        """

        Outputs = {}
        #loop through each node in the tree
        for node in self.nodes:
            #if node is a leaf execute the pipeline from it to the root
            if node.is_a_leaf:
                index = node.name.split("-")[1]
                index = int(index)
                result = self.execute_path(data_input, index)
                Outputs[node.name] = result

        return Outputs

#------------------------------------------------------------------------------

#created functions that deal with the Tree class
def copy_subtree(main_tree: TS_Tree, node_index: int):
    """
    Takes a Tree and returns a copy of the subtree starting at node (node_index)
    as a new TS_Tree object.

    Calls:
        tree.py - save_tree()
    Call By:

    Returns - Tree
    """
    sub_tree = TS_Tree()

    #check to make sure node_index is valid
    if node_index >= len(main_tree.nodes) or node_index < 0:
        print("Invalid node_index")
        return None

    #set up root node
    root = main_tree.nodes[node_index]
    new_node = root.copy_node()
    new_node.parent = None

    #set up sub_tree
    sub_tree.nodes[0] = new_node

    #get list of nodes that will make up the subtree
    node_list = root.get_decendents()
    for node in node_list:
        #create a copy of the node
        copy = node.copy_node()
        #get copy to point to the parent copy
        for node in sub_tree.nodes:
            if node.name == copy.parent.name:
                copy.parent = node
        sub_tree.nodes.append(copy)

    #reset indexes of Nodes
    for node_i in range(len(sub_tree.nodes)):
        node = sub_tree.nodes[node_i]
        node_info = node.name.split("-")
        node_operation = node_info[0]
        node.name = node_operation + "-" + str(node_i)

    return sub_tree

def add_subtree(tree: TS_Tree, node_index: int, sub_tree: TS_Tree):
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
    if node_index > len(tree.nodes) or node_index < 0:
        print("Invalid node_index")
        return None

    #connect sub_tree to tree
    sub_tree.nodes[0].parent = tree.nodes[node_index]
    for node in sub_tree.nodes:
        tree.nodes.append(node)

    #reset indexes of Nodes
    for node_i in range(len(tree.nodes)):
        node = tree.nodes[node_i]
        node_info = node.name.split("-")
        node_operation = node_info[0]
        node.name = node_operation + "-" + str(node_i)

def copy_path(main_tree: TS_Tree, node_index: int):
    """
    Takes a Tree and returns a copy of the path starting at the root and going
    to (node_index) as a new TS_Tree object.

    Calls:
        tree.py - TS_Tree.get_path()
    Call By:

    Returns - Tree
    """
    path_copy = TS_Tree()

    #check to make sure node_index is valid
    if node_index > len(main_tree.nodes) or node_index < 0:
        print("Invalid node_index")
        return None

    #get list of nodes that will make up the subtree
    node_list = main_tree.get_path(node_index)
    for node in node_list:
        #create a copy of the node
        copy = node.copy_node()

        #root condition
        if node.parent == None:
            path_copy.nodes[0] = copy
        else:
            #get copy to point to the parent copy
            for node in path_copy.nodes:
                if node.name == copy.parent.name:
                    copy.parent = node
            path_copy.nodes.append(copy)

    #reset indexes of Nodes
    for node_i in range(len(path_copy.nodes)):
        node = path_copy.nodes[node_i]
        node_info = node.name.split("-")
        node_operation = node_info[0]
        node.name = node_operation + "-" + str(node_i)

    return path_copy

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
        save_file.write(f"{node.function_inputs[8]},")
        save_file.write(f"{node.function_inputs[9]},")
        save_file.write(f"{node.function_inputs[10]},")
        save_file.write(f"{node.function_inputs[11]},")
        save_file.write(f"{node.function_inputs[12]}\n")

    save_file.close()

def load_tree(save_file_name: str):
    """
    Function to load tree stucture from given file (save_file_name).

    Calls:
        None
    Call By:
        TS_Tree()
        TS_Tree.add_node()

    Return - TS_Tree
    """

    loaded_tree = TS_Tree()

    try:
        load_file = open(save_file_name, "r")
        Lines = load_file.readlines()
        for line in Lines:
            line = line.strip().split(',')

            node_info = line[0].split('-')
            node_operation = node_info[0]
            node_index = node_info[1]

            #get the function parameters

            #data_start
            if line[2] == "None":
                data_start = None
            else:
                data_start = float(line[2])

            #data_end
            if line[3] == "None":
                data_end = None
            else:
                data_end= float(line[3])

            #increment
            if line[4] == "None":
                increment = None
            else:
                increment = float(line[4])

            #perc_training
            if line[5] == "None":
                perc_training = None
            else:
                perc_training = float(line[5])

            #perc_valid
            if line[6] == "None":
                perc_valid = None
            else:
                perc_valid = float(line[6])

            #perc_test
            if line[7] == "None":
                perc_test = None
            else:
                perc_test = float(line[7])

            #input_filename
            if line[8] == "None":
                input_filename = None
            else:
                input_filename = line[8]

            #output_filename
            if line[9] == "None":
                output_filename = None
            else:
                output_filename = line[9]

            #m_i
            if line[10] == "None":
                m_i = None
            else:
                m_I = float(line[10])

            #t_i
            if line[11] == "None":
                t_i = None
            else:
                t_i = float(line[11])

            #m_0
            if line[12] == "None":
                m_0 = None
            else:
                m_0 = float(line[12])

            #t_0
            if line[13] == "None":
                t_0 = None
            else:
                t_0 = float(line[13])

            #layers
            if line[14] == "None":
                layers = None
            else:
                layers = []
                layers.append(float(line[14][1:]))
                for i in range(15, len(line)):
                    if i == len(line) - 1:
                        layers.append(float(line[i][:-1]))
                    else:
                        layers.append(float(line[i]))

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
                               m_i,
                               t_i,
                               m_0,
                               t_0,
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
                                     perc_training = perc_training,
                                     perc_valid = perc_valid,
                                     perc_test = perc_test,
                                     input_filename = input_filename,
                                     output_filename = output_filename,
                                     m_i = m_i,
                                     t_i = t_i,
                                     m_0 = m_0,
                                     t_0 = t_0,
                                     layers = layers)

        load_file.close()

    except:
        print(f"\nError loading {save_file_name} - Bad Format\n")
        return

    return loaded_tree
