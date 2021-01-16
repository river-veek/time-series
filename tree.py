"""

"""

# anytree library being used to get RenderTree functionality for printing a repersentation of the tree
from anytree import Node, RenderTree, NodeMixin

class Operation_node(NodeMixin):
    """
    Operation_node is a node class built off of the basic anytree node class
    that includes aditionaly functionality for storing function calls
    """

    def __init__(self, name, depth: int, patent = None):
        """
        name is a string in the form - 'operation_call-node_index'
        """
        super(Operation_node, self).__init__()
        self.name = name
        self.depth = depth
        self.parent = parent
        self.child_list = []

    def add_child(self, new_node):
        self.child_list.append(new_node)

    def change_operation(self, new_operation):
        """
        Function to replace the operation string of the node with (new_operation)

        Returns - None
        """
        #pull out node index
        node_index = self.name.split('-')[1]

        #create new node name string
        new_name = f"{new_operation}-{node_index}"
        self.name = new_name

    def get_operation(self):
        """
        Function to pull out the operation string of the node

        Returns - str
        """
        operation = node_index = self.name.split('-')[0]
        return(operation)

    def get_decendents(self):
        decendent_list = []

        for child in self.child_list:
            decendent_list.append(child)
            decendent_list += child.get_decendents()

        return decendent_list

class Tree:

    def __init__(self):
        """
        Initilize a Tree with a blank root node
        """
        #make empty root node and place it in the Tree
        root_node = Operation_node("no_operation-0", None)
        self.nodes = [root_node]
        self.hight = 0

    def print_tree(self):
        """
        Function for displaying a string repersentation of the tree

        Returns - None
        """
        for pre, fill, node in RenderTree(self.nodes[0]):
            print("%s%s" % (pre, node.name))

    def add_node(self, operation: str, parent_index: int):
        """
        Function for adding a new node to the tree. Takes a operation string and
        the index of the parent (parent_index). New node gets added as a child
        of the parent and added into the list of tree nodes.

        Returns - None
        """
        #check to make sure parent_index is valid
        if parent_index > len(self.nodes) or node_index < 0:
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

        Returns - None
        """
        #check to make sure node_index is valid
        if node_index > len(self.nodes) or node_index < 0:
            print("Invalid node_index")
            return None

        node = self.nodes[node_index]
        node.change_operation(new_operation)
