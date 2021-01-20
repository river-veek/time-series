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
                  "design_matrix",
                  "ts2db",
                  "mlp_model"]

visualization = ["plot",
                 "histogram",
                 "box_plot",
                 "normality_test",
                 "mse",
                 "mape",
                 "smape"]


def print_operation_lists():
    """
    Function to display to terminal the valid pre-processing and visualization
    operation inputs

    Calls - None
    Call By - get_user_operation()

    Returns - None
    """

    print("\n###Operation List###")

    print("  #Pre-Proccessing#")
    for i in range(0, len(pre_processing), 2):
        if i < len(pre_processing) - 1:
            print(f"\t{pre_processing[i]} ---- {pre_processing[i+1]}")
        else:
            print(f"\t{pre_processing[i]}")

    print("  #Visualization#")
    for i in range(0, len(visualization), 2):
        if i < len(visualization) - 1:
            print(f"\t{visualization[i]} ---- {visualization[i+1]}")
        else:
            print(f"\t{visualization[i]}")

def get_user_operation():
    """
    Function to get operation user inputs

    If invalid user input returns None

    Calls - print_operation_lists()
    Call By - main()

    Returns - str
    """
    #print valid operation lists
    print_operation_lists()

    #get operation for root node
    operation = input("Type operation you wish to enter for root node: ").strip()
    if (operation not in pre_processing) and (operation not in visualization):
        print(f"Error - {operation} is an Invalid Input")
        return None

    return operation

def get_user_index(node_type: str):
    """
    Function to get a valid index of node user inputs. node_type is either
    'parent', or 'node' to determine message for user

    If invalid user input returns None

    Calls - None
    Call By - main()

    Returns - int
    """

    #get index of target node
    if node_type == 'parent':
        node_index = input("Enter index of parent to add node to: ").strip()
    else:
        node_index = input("Enter index of node to edit: ").strip()

    #check that node_index is an int
    try:
        node_index = int(node_index)
    except:
        print(f"Error - {node_index} is not an Integer")
        return None

    return node_index

def main():

    tree = None
    while(1==1):
        print("\n###Current Tree###")
        if tree == None:
            print("No tree currently loaded\n")
        else:
            tree.print_tree()
            print()

        print("###Command List###")
        print("\tTo create tree type 'create'")
        print("\tTo clear tree type 'clear'")
        print("\tTo load tree type 'load'")
        print("\tTo save tree type 'save'")
        print("\tTo replace a node in the tree type 'replace'")
        print("\tTo add a node to the tree type 'add'")
        print("\tTo execute a tree or tree branch type 'execute_tree'")
        print("\tTo close this program type 'quit'")
        print()

        user_command = input("Please enter the command you wish to preform: ").strip()

        if user_command == "create":
            operation = get_user_operation()
            #if vaid operation
            if operation != None:
                #create empty tree
                tree = Tree()
                #replace blank operation in root with user input
                tree.replace_node(operation, 0)

        elif user_command == "clear":
            tree = None

        elif user_command == "load":
            tree_file = input("Please enter name of tree save file to load: ").strip()
            tree = load_tree(tree_file)

        elif user_command == "save":
            save_file = input("Please enter name of save file to save tree into: ").strip()
            save_tree(tree, save_file)

        elif user_command == "replace":
            node_index = get_user_index("node")
            operation = get_user_operation()

            #if vaid operation
            if (operation != None) and (node_index != None):
                tree.replace_node(operation, node_index)

        elif user_command == "add":
            node_index = get_user_index("parent")
            operation = get_user_operation()

            #if vaid operation
            if (operation != None) and (node_index != None):
                tree.add_node(operation, node_index)

        elif user_command == "execute_tree":
            pass
        elif user_command == "quit":
            break
        else:
            print("\n---Invalid Command---\n")


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

#test()
main()
