# For this program, I chose the red black tree to store all the events the user can encounter, and they are stored
# from left to right chronologically, and if there are multiple events with the same chronological estimate, they are stored in a duplicate list.
# I used recursion for all of the functions in this tree and implemented the insert, retrieve and display functions.
# In the program I use 16 total encounters but if I scaled this game up and made it longer/more complex it would still have
# good performance due to the use of a red black tree instead of a simple binary search tree.

class Node:
    def __init__(self, event, color):
        self.__event = event  # Store's the event of the node and we will sort the nodes by the event's chronological estimate (boss node will be rightmost)
        self.__color = color  # Red or black, used to balance the tree
        self.__parent = None  # Parent initialized to None
        self.__left = None  # Left child initialized to None
        self.__right = None  # Right child initialized to None
        self.__duplicate_list = []  # List of duplicate events (chronologically have the same priority)

    def get_left(self):
        return self.__left
    
    def get_right(self):
        return self.__right
    
    def get_parent(self):
        return self.__parent
    
    def get_event(self):
        return self.__event
    
    def get_color(self):
        return self.__color
    
    def get_duplicates(self):
        return self.__duplicate_list
    
    def add_duplicate(self, to_add):
        return self.__duplicate_list.append(to_add)
    
    def set_left(self, left):
        self.__left = left
        return True

    def set_right(self, right):
        self.__right = right
        return True

    def set_parent(self, parent):
        self.__parent = parent
        return True

    def set_event(self, event):
        self.__event = event
        return True
    
    def set_color(self, color):
        self.__color = color
        return True
    
    def pop_duplicate(self):
        return self.__duplicate_list.pop()

class RedBlackTree:
    def __init__(self):
        self.__root = None # Set root to "null" or None

    def get_root(self):
        return self.__root
    
    def set_root(self, to_set):
        self.__root = to_set

    def insert(self, event):
        to_insert = Node(event, color='red') # Initialize to red

        if self.get_root() is None: # If empty tree
            to_insert.color = 'black' # Root always black so we change node to black
            self.set_root(to_insert)
            return True
        else:
            self.__insert_helper(self.get_root(), to_insert) # Recursive insert by chronological order
            return self.__fix_tree(to_insert) # Uses rotate-left and rotate-left with logic to fix the insert in its own function  

    def get_event(self, chronological): # Returns an event by the chronological estimate
        return self.__get_event_helper(chronological, self.get_root())
            
    def display(self):
        if self.get_root() is None:
            print("Cannot print empty tree.\n")
            return False
        return self.__rec_display_helper(self.get_root())

    def __insert_helper(self, temp, to_insert):
        if to_insert.get_event().get_chronological() == temp.get_event().get_chronological(): # If duplicate priority
            temp.add_duplicate(to_insert) # Add to duplicate list
            return False
        if to_insert.get_event().get_chronological() < temp.get_event().get_chronological(): # If before chronologically
            if temp.get_left() is None:
                temp.set_left(to_insert) 
                to_insert.set_parent(temp)
                return True
            else:
                return self.__insert_helper(temp.get_left(), to_insert) # Recursively call
        else: # If after chronologically
            if temp.get_right() is None:
                temp.set_right(to_insert)
                to_insert.set_parent(temp)
                return True
            else:
                return self.__insert_helper(temp.get_right(), to_insert) # Recursively call

    def __fix_tree(self, node): # Fixes the tree by rotating nodes and changing colors recursively
        to_return = self.__fix_tree_helper(node) 
        self.get_root().set_color('black') # Root must always be black in red black tree so we set to black after recursive call done
        return to_return

    def __fix_tree_helper(self, node):
        if node != self.get_root() and node.get_parent().get_color() == "red": # We need to rotate if if the node is non-root and its parent is red
            parent = node.get_parent()
            grandparent = parent.get_parent()
            if grandparent is None: # This means the parent is the root and we don't need to fix anymore
                return True
            if parent == grandparent.get_left(): # If parent is the left child then that means uncle is a right child
                uncle = grandparent.get_right()
                if uncle and uncle.get_color() == "red":
                    parent.set_color("black") # If red uncle then we move it's red up and rotate the grandparent to fix the red to black 
                    uncle.set_color("black")
                    grandparent.set_color("red")
                    return self.__fix_tree_helper(grandparent) # Recursively call until whole tree is fixed
                else:
                    if node == parent.get_right(): # If right child
                        node = parent
                        self.__left_rotate(node) # Rotate left
                    parent.set_color("black")
                    grandparent.set_color("red")
                    self.__right_rotate(grandparent)
                    return self.__fix_tree_helper(node) # Recursively call
            else:
                uncle = grandparent.get_left()
                if uncle and uncle.get_color() == "red": # Same as above but inverse
                    parent.set_color("black")
                    uncle.set_color("black")
                    grandparent.set_color("red")
                    return self.__fix_tree_helper(grandparent) # Recursively call
                else:
                    if node == parent.get_left(): # If left child
                        node = parent
                        self.__right_rotate(node) # Rotate right
                    parent.set_color("black")
                    grandparent.set_color("red")
                    self.__left_rotate(grandparent)
                    return self.__fix_tree_helper(node) # Recursively call
        return True # If node's parent is not red and is not the root we don't need to continue traversing

    def __left_rotate(self, to_become_left): # If node and its parent are red then we rotate left depending on if left or right parent
        temp = to_become_left.get_right() # Stores original right which will become new "root" of subtree
        to_become_left.set_right(temp.get_left()) # Connects the left of the new "root" to the right of the original "root"
        if temp.get_left() is not None: # If the left of the new "root" is not None, we set it's parent to the original "root"
            temp.get_left().set_parent(to_become_left)
        temp.set_parent(to_become_left.get_parent()) # Set the parent of the new "root" to the parent of the original "root"
        if not to_become_left.get_parent(): # If the original "root" was the root of the entire tree then we assign the "new" root to be the tree's root
            self.set_root(temp)
        elif to_become_left == to_become_left.get_parent().get_left(): # If original "root" is left child
            to_become_left.get_parent().set_left(temp) # Set parent's left to new "root"
        else: # If original "root" is right child
            to_become_left.get_parent().set_right(temp) # Set parent's right to new "root"
        temp.set_left(to_become_left) # Set the left of the new "root" to the original "root"
        to_become_left.set_parent(temp)
        return True

    def __right_rotate(self, to_become_right): # Same as above but for opposite parents
        temp = to_become_right.get_left() # We do all of the operations above but inversed
        to_become_right.set_left(temp.get_right())
        if temp.get_right() is not None:
            temp.get_right().set_parent(to_become_right)
        temp.set_parent(to_become_right.get_parent())
        if not to_become_right.get_parent():
            self.set_root(temp)
        elif to_become_right == to_become_right.get_parent().get_left():
            to_become_right.get_parent().set_left(temp)
        else:
            to_become_right.get_parent().set_right(temp)
        temp.set_right(to_become_right)
        to_become_right.set_parent(temp)
        return True

    def __get_event_helper(self, chronological, node=None): # Recursive private helper for returning an event by chronological estimate
        if node is None:
            print("Cannot find from empty tree.")
            return False

        if chronological == node.get_event().get_chronological():
            return node.get_event()  # Found the event
        elif chronological < node.get_event().get_chronological():
            if(node.get_left()): 
                return self.__get_event_helper(chronological, node.get_left()) # Event before chronologically
            else: 
                print("Event not found.")
                return False
        else:
            if(node.get_right()): 
                return self.__get_event_helper(chronological, node.get_right()) # Event after chronologically
            else:
                print("Event not found.")
                return False

    def __rec_display_helper(self, node):
        if node is None:
            return True
        self.__rec_display_helper(node.get_left())
        print("--------------------")
        print(f"Event: {node.get_event()}Chronological order: {node.get_event().get_chronological()}, Character: {node.get_event().get_character().get_name()}, Encounter type: {node.get_event().get_type()}, Color: {node.get_color()}")
        print("--------------------")
        self.__rec_display_helper(node.get_right())
        return True