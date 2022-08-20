# Python program to introduce Binary Search Tree (BST)

# See for details: https://www.geeksforgeeks.org/binary-search-tree-data-structure/?ref=lbp 
 
# A class that represents an individual node
# in a Binary Tree
class Node:
    def __init__(self, key):
        self.left = None
        self.right = None
        self.val = key

    def get_left_child(self):
      return self.left

    def set_left_child(self, left):
        self.left = left

    def get_right_child(self):
        return self.right

    def set_right_child(self,right):
        self.right = right
    
    def get_value(self):
        return self.val
    
    def set_value(self, value):
        self.val = value
    
    def print_tree(self):
        if self.left:
            self.left.print_tree()
        
        print(self.val)

        if self.right:
            self.right.print_tree()

# Main BST operations

def insert(head, node):
    if head == None:
        return node
    if node.get_value() <= head.get_value():
        head.set_left_child(insert(head.get_left_child(), node))
        print ('AELZ_01 set LEFT child for head::node {}::{}'.format( head.get_value(), node.get_value()))
    else:
        head.set_right_child(insert(head.get_right_child(), node))
        print ('AELZ_02 set RIGHT child for head::node {}::{}'.format(head.get_value(), node.get_value()))

    
    return head

def lookup(head, data):
    if head == None:
        return print("Value not found!")
    if head.get_value() == data:
        return head
    if data <= head.get_value():
        return lookup(head.get_left_child(), data)
    else:
        return lookup(head.get_right_child(), data)

# Left most element in BST
def min_value(head):
    current = head
    # loop down to find the leftmost leaf
    while(current.left != None):
        current = current.left 
    return current.val

# Right most element in BST
def max_value( head):
    current = head
    # loop down to find the rightmost leaf
    while(current.right != None):
        current = current.right
    return current.val


def print_node(node):
    if (node == None):
        print("Not found!")
    print(node.get_value())

 
# Breadth First Traveral, BST (shirina)
class MyQueue:
    def __init__(self):
        """ Create a new queue. """
        self.items = []

    def is_empty(self):
        """ Returns true if queue is empty """
        return len(self.items) == 0
    
    def enqueue(self, item):
        """ Add a new element to the end of queue. """
        self.items.append(item)
    
    def dequeue(self):
        """ Remove a element from the beginning of queue. """
        return self.items.pop(0)

    def size(self):
        """ Returns the size of the queue. """
        return len(self.items)

    def peek(self):
        """ Have a look at first element of the queue. """
        if self.is_empty():
            raise Exception("Nothing to peek")
        return self.items[0]

def breadth_first(node):
    if (node == None):
        raise Exception("No root found!")
    path = []
    queue = MyQueue()
    queue.enqueue(node)
    while queue.size() > 0:
        current = queue.dequeue()
        path.append(current.val)
        if current.get_left_child() != None:
            queue.enqueue(current.get_left_child())
        if current.get_right_child() != None:
            queue.enqueue(current.get_right_child())
    return path

if __name__ == '__main__':

    A = Node(45)
    B = Node(2)
    C = Node(33)
    D = Node(54)
    E = Node(25)
    F = Node(68)
    G = Node(72)
    H = Node(81)
    I = Node(23)
   

    # Create root / head 
    head = insert(None, E)
    insert(head, B)
    insert(head, A)
 
    ''' following is the tree after above statement
        25
      /   \
     2    45'''
    
    insert(head, C)
    insert(head, D)
    insert(head, F)
    insert(head, G)
    insert(head, H)
    insert(head, I)
    head.print_tree()

    ''' 
           25
         /   \
        2      45
         \    /  \
         23  33   54
          \    \   \
          68   72   81

  '''



    print('\n Lookup 68 node*****')
    print_node(lookup(head, 68))
    # print_node(lookup(head, 10))

    print('\n Min/ max  value *****')
    print(min_value(head))
    print(max_value(head))

    print('\n Breadth First Traversal *****')
    print(breadth_first(E))