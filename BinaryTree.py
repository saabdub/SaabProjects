
"""
Simple binary search tree implementation.

"""

class treeNode:
    def __init__(self, data):
        self.root = data
        self.left = None
        self.right = None

    def is_empty(self) -> bool:
        return self.root == self.left == self.right == None

    def is_leaf(self) -> bool:
        return self.left == self.right == None

    def size(self)-> int:
        if self.is_empty():
            return 0
        else:
            return 1 + self.left.size() + self.right.size()











