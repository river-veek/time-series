from tree import *

def print_operation_lists():
    """
    Function to display to terminal the valid pre-processing and visualization
    operation inputs

    Calls:
        None
    Call By:
        user_interface.py - get_user_operation()

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

    Calls:
        user_interface.py - print_operation_lists()
    Call By:
        user_interface.py - main()

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

def get_user_index(command_str: str):
    """
    Function to get a valid index of node user inputs. command_str is the string
    to print out to promp user input

    If invalid user input returns None

    Calls:
        None
    Call By:
        User_interface.py - main()

    Returns - int
    """

    #get index of target node
    node_index = input(command_str).strip()

    #check that node_index is an int
    try:
        node_index = int(node_index)
    except:
        print(f"Error - {node_index} is not an Integer")
        return None

    return node_index

def main():

    tree = None
    ts = None
    while(1==1):
        print("\n###Current Tree###")
        if tree == None:
            print("No tree currently loaded\n")
        else:
            tree.print_tree()
            print()

        print("###Command List###")
        print("\tTo load a time series type 'ts'")
        print("\t--------------------------")
        print("\tTo create tree type 'create'")
        print("\tTo clear tree type 'clear'")
        print("\tTo load tree type 'load'")
        print("\tTo save tree type 'save'")
        print("\t--------------------------")
        print("\tTo replace a node in the tree type 'replace'")
        print("\tTo add a node to the tree type 'add_node'")
        print("\tTo add a sub-tree to the tree type 'add_subtree'")
        print("\t--------------------------")
        print("\tTo execute a tree or tree branch type 'execute_tree'")
        print("\tTo close this program type 'quit'")
        print()

        user_command = input("Please enter the command you wish to preform: ").strip()

        if user_command == "ts":
            ts_file = input("Please enter name of ts file to load: ").strip()

        elif user_command == "create":
            operation = get_user_operation()
            #if vaid operation
            if operation != None:
                #create empty tree
                tree = TS_Tree()
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
            command_str = "Enter index of node to replace: "
            node_index = get_user_index(command_str)
            operation = get_user_operation()

            #if vaid operation
            if (operation != None) and (node_index != None):
                tree.replace_node(operation, node_index)

        elif user_command == "add_node":
            #get user inputs
            command_str = "Enter index of parent to add node to: "
            node_index = get_user_index(command_str)
            operation = get_user_operation()

            #if vaid operation
            if (operation != None) and (node_index != None):
                tree.add_node(operation, node_index)

        elif user_command == "add_subtree":
            tree_file = input("Please enter name of tree save file to load as subtree: ").strip()
            subtree = load_tree(tree_file)

            command_str = "Enter index of node to add subtree to: "
            node_index = get_user_index(command_str)

            #if vaid operation
            if (operation != None) and (node_index != None):
                tree.add_node(operation, node_index)

        # elif user_command == "copy_subtree":
        #
        #     command_str = "Enter index of root of target subtree: "
        #     node_index = get_user_index(command_str)
        #
        #     save_file = input("Please enter name of save file to save subtree into: ").strip()
        #     subtree = load_tree(tree_file)
        #
        #     #if vaid operation
        #     if (operation != None) and (node_index != None):
        #         tree.add_node(operation, node_index)


        elif user_command == "execute_tree":
            pass
        elif user_command == "quit":
            break
        else:
            print("\n---Invalid Command---\n")

main()
