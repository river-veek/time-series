from tree import *

pre_processing = ["denoise",
                  "input_missing_data",
                  "input_outliers",
                  "longest_continous_run",
                  "clip",
                  "assign_time",
                  "difference",
                  "scaling",
                  "standardize",
                  "logarithm",
                  "cubic_root",
                  "split_data",
                  "design_matrix"]

#idea! nodes store the type of function call.
##To exicute a path user specifies the nodes the end node that they want to reach
## the system will then go through the tree collecting the name of the operations to call
def copy_subtree(main_tree: Tree, node_index: int):
    """
    Takes a Tree and returns a copy of the subtree starting at node (node_index)

    Inputs - Tree, node_index
    Returns - Tree
    """
    sub_tree = Tree()

    new_root = main_tree.nodes[node_index]
    new_root.parent = None

    node_list = new_root.get_decendents()

    #set up sub_tree
    sub_tree.nodes[0] = new_root
    sub_tree.nodes += node_list

    return sub_tree

def add_subtree(tree: Tree, node_index: int, subtree: Tree):
    """

    """


def save_tree(tree: Tree, save_file_name: str):
    """
    Function to save target tree (tree) stucture into a file named (save_file_name).

    The resulting save_file will save each node on a line as follows
        'node.name,parent.name'
    """

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

def load_tree(save_file_name: str):
    """
    Function to load tree stucture from given file (save_file_name).

    Return - Tree
    """

    #open file to write the tree data file
    load_file = open(save_file_name, "r")

    loaded_tree = Tree()

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

    return loaded_tree

def test():

    #test basic tree build
    test_tree = Tree()
    test_tree.add_node("first_node", 0)
    test_tree.add_node("secound_node", 0)
    test_tree.add_node("third_node", 1)
    test_tree.add_node("fourth_node", 1)
    test_tree.add_node("fith_node", 4)
    test_tree.add_node("sixth_node", 4)
    test_tree.print_tree()

    #test replacing a node operation
    test_tree.replace_node("replaced", 5)
    test_tree.print_tree()

    save_tree(test_tree, "save_file.txt")

    loaded_tree = load_tree("save_file.txt")
    print("Loaded Tree:")
    loaded_tree.print_tree()

    print("Sub-Tree:")
    sub_tree = copy_subtree(test_tree, 1)
    sub_tree.print_tree()

test()
