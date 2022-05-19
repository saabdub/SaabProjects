
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











