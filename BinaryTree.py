
"""
Simple binary search tree implementation.

"""

class treeNode:
    """
    Inserts a new node into the tree.
    """
    def __init__(self):
        self.root = None
        self.left = None
        self.right = None


def is_empty(btree: treeNode) -> bool:
    """
    Returns True if the tree is empty.
    :param btree: which is a treeNode
    :return: bool
    """
    return btree.root == btree.left == btree.right == None


def is_leaf(btree: treeNode) -> bool:
    """
    Returns True if the tree is a leaf.
    :param btree: which is a treeNode
    :return: bool
    """
    return btree.left == btree.right == None


def size(btree: treeNode) -> int:
    """
    Returns the size of the tree.
    :param btree: which is a treeNode
    :return: int
    """
    if is_empty(btree):
        return 0
    elif is_leaf(btree):
        return 1
    else:
        return 1 + size(btree.left) + size(btree.right)

def is_exists(btree: treeNode, key: object) -> bool:
    """Return True if and only if a node of tree has the key.
    :return: bool
    """
    if is_empty(btree):
        return False
    elif btree.root[0] == key:
        return True
    elif is_leaf(btree):
        return False
    elif btree.root[0] < key :
        return is_exists(btree.right, key)
    else:
        return is_exists(btree.left, key)

def insertIntoTree(btree: treeNode, key: object, value: object)-> None:
    """
    Inserts a new node into the tree.
    :param btree: which is a treeNode
    :param key: which is an object
    :param value: which is an object
    :return: None
    """
    if is_empty(btree):
        btree.root = (key, value)
        btree.left = treeNode()
        btree.right = treeNode()
    elif btree.root[0] == key:
        btree.root = (key, value)
    elif btree.root[0] < key:
        insertIntoTree(btree.right, key, value)
    else:
        insertIntoTree(btree.left, key, value)

def findTheSmallest(btree: treeNode) -> object:
    """
    Returns the smallest key in the tree.
    :param btree: which is a treeNode
    :return: root of the object
    """
    if is_empty(btree):
        return None
    elif not is_leaf(btree):
        return findTheSmallest(btree.left)
    else:
        return btree.root[0]

def lookup(btree: treeNode, key: object) -> object:
    """
    Returns the value associated with the key.
    :param btree: which is a treeNode
    :param key: which is an object
    :return: value of the object
    """
    if is_empty(btree):
        return None
    elif btree.root[0] == key:
        return btree.root[1]
    elif btree.root[0] < key:
        return lookup(btree.right, key)
    else:
        return lookup(btree.left, key)



def printInOrder(btree: treeNode) -> None:
    """Print tree contents in order."""

    if is_empty(btree):
        return
    if btree.left:
        printInOrder(btree.left)
        print(btree.root)
        if btree.right:
            printInOrder(btree.right)
    elif btree.right:
        print(btree.root)
        printInOrder(btree.right)
    else:
        print(btree.root)



