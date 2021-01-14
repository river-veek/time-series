"""

"""

# anytree library being used to get RenderTree functionality for printing a repersentation of the tree
from anytree import Node, RenderTree, NodeMixin

class Operation_node(NodeMixin):
    """
    Operation_node is a node class built off of the basic anytree node class
    that includes aditionaly functionality for storing function calls
    """

    def __init__(self, name, parent=None, children=None):
        """
        name is a string in the form - 'operation_call-node_index'
        """
        super(Operation_node, self).__init__()
        self.name = name
        self.parent = parent
        # set children only if given
        if children != None:
            self.children = children

    def add_child(self, new_node):
        self.child_nodes.append(new_node)

    def change_operation(self, new_operation):
        node_index = self.name.split('-')[1]
        new_name = f"{new_operation}-{node_index}"
        self.name = new_name

    def get_operation(self):
        operation = node_index = self.name.split('-')[0]
        return(operation)

class Tree:

    def __init__(self):
        #make empty root node and place it in the Tree
        root_node = Operation_node("no_operation-0", None, None)
        self.nodes = [root_node]

    def print_tree(self):
        #print(RenderTree(self.nodes[0]))
        for pre, fill, node in RenderTree(self.nodes[0]):
            print("%s%s" % (pre, node.name))

    def add_node(self, operation, parent_index):
        parent_node = self.nodes[parent_index]
        new_node_name = f"{operation}-{len(self.nodes)}"
        new_node = Operation_node(new_node_name, parent_node)
        self.nodes.append(new_node)

    def replace_node(self, new_operation, node_index):
        if node_index > len(self.nodes) or node_index < 0:
            print("Invalid node_index")
            return None

        node = self.nodes[node_index]
        node.change_operation(new_operation)


def test():

    #test basic tree build
    test_tree = Tree()
    test_tree.add_node("first_node", 0)
    test_tree.add_node("secound_node", 0)
    test_tree.add_node("third_node", 1)
    test_tree.add_node("fourth_node", 1)
    test_tree.add_node("fith_node", 1)
    test_tree.add_node("fith_node", 1)
    test_tree.print_tree()

    #test replacing a node operation
    test_tree.replace_node("replaced", 5)
    test_tree.print_tree()

test()
