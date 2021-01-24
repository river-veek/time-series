"""

"""

# anytree library being used to get RenderTree functionality for printing a repersentation of the tree
from anytree import Node, RenderTree, NodeMixin
import os
import shutil

class Operation_node(NodeMixin):
    """
    Operation_node is a node class for a Tree built off of the basic
    anytree node class. Operation_node class includes aditionaly functionality
    for storing function calls and node depth then NodeMixin
    """

    def __init__(self, name: str, depth: int, parent = None):
        """
        Initilize node properties: (name, depth, parent, child_list)
            name is a string in the form - 'operation_call-node_index'
            depth is an int repersenting how deap in the tree the node it
            parent is a Operation_node (can be None) that is the parent
            child_list is an empty list to store child nodes
        """
        super(Operation_node, self).__init__()
        self.name = name
        self.node_depth = depth
        self.parent = parent
        self.child_list = []

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

    def change_operation(self, new_operation: str):
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

    def get_operation(self):
        """
        Function to pull out and return the operation string of the node

        Calls:
            None
        Call By:
            ___

        Returns - str
        """
        operation = node_index = self.name.split('-')[0]
        return(operation)

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
        Initilize a Tree with a blank root node
        """
        #make empty root node and place it in the Tree
        root_node = Operation_node("no_operation-0", 0, None)
        self.nodes = [root_node]
        self.hight = 0

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

    def add_node(self, operation: str, parent_index: int):
        """
        Function for adding a new node to the tree. Takes a operation string and
        the index of the parent (parent_index). New node gets added as a child
        of the parent and added into the list of tree nodes.

        Calls:
            tree.py - Operation_node.__init__(name, depth, parent_node)
            tree.py - Operation_node.add_child(Operation_node)
        Call By:
            User_interface.py - main()
            tree.py - add_subtree()

        Returns - None
        """
        #check to make sure parent_index is valid
        if parent_index > len(self.nodes) or parent_index < 0:
            print("Invalid parent_index")
            return None

        #get the parent node based off of the parent index
        parent_node = self.nodes[parent_index]

        #set up name for the new node depending of the given operation and the
        ## number of nodes currently in the tree
        new_node_name = f"{operation}-{len(self.nodes)}"
        new_node_depth = parent_node.depth + 1

        #create and add new node to the tree
        new_node = Operation_node(new_node_name, new_node_depth, parent_node)
        parent_node.add_child(new_node)

        self.nodes.append(new_node)
        if new_node_depth > self.hight:
            self.hight = new_node_depth

    def replace_node(self, new_operation: str, node_index: int):
        """
        Function to replace the operation with (new_operation) of the
        (node_index) node within the tree

        Calls:
            tree.py - Operation_node.change_operation(new_operation)
        Call By:
            User_interface.py - main()

        Returns - None
        """
        #check to make sure node_index is valid
        if node_index > len(self.nodes) or node_index < 0:
            print("Invalid node_index")
            return None

        node = self.nodes[node_index]
        node.change_operation(new_operation)

#------------------------------------------------------------------------------

#created functions that deal with the Tree class
def copy_subtree(main_tree: TS_Tree, node_index: int, save_file_name: str):
    """
    Takes a Tree and returns a copy of the subtree starting at node (node_index)
    in a save file named (save_file_name) in the TreeFiles folder.

    Calls:
        tree.py - save_tree()
    Call By:
        User_interface.py - main()

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

    """


def save_tree(tree: TS_Tree, save_file_name: str):
    """
    Function to save target tree (tree) stucture into a file named (save_file_name).
    The resulting save_file will save each node on a line as follows
        'node.name,parent.name'

    Calls:
        None
    Call By:
        User_interface.py - main()
        tree.py - copy_subtree()

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
            save_file.write(f"{node.name},None\n")
        else:
            save_file.write(f"{node.name},{node.parent.name}\n")
    save_file.close()

    #move save file into TreeFiles folder
    store_loc = os.getcwd()+ "/TreeFiles"
    shutil.move(save_file_name, store_loc)

def load_tree(save_file_name: str):
    """
    Function to load tree stucture from given file (save_file_name).

    Calls:
        None
    Call By:
        User_interface.py - main()

    Return - TS_Tree
    """

    #open file to write the tree data file
    try:
        path_to_file = os.getcwd()+ "/TreeFiles/" + save_file_name
        load_file = open(path_to_file, "r")
    except:
        print(f"\nError loading {save_file_name} - Not Found\n")
        return None

    try:
        loaded_tree = TS_Tree()

        Lines = load_file.readlines()
        for line in Lines:
            line = line.strip().split(',')

            node_info = line[0].split('-')
            node_operation = node_info[0]
            node_index = node_info[1]

            #root node condition
            if node_index == '0':
                loaded_tree.nodes[0].change_operation(node_operation)
            else:
                parent_info = line[1].split('-')
                parent_index = int(parent_info[1])
                loaded_tree.add_node(node_operation, parent_index)

        load_file.close()
    except:
        print(f"\nError loading {save_file_name} - Bad Format\n")
        return None

    return loaded_tree
