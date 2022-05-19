import BinaryTree as b


def classtest(item):
    tree = b.treeNode()
    assert b.is_empty(tree) == True
    assert b.is_leaf(tree) == True
    assert b.size(tree) == 0
    tree2 = b.treeNode()
    tree2.root = "a"
    assert b.is_empty(tree2) == False
    assert b.is_leaf(tree2) == True
    assert b.size(tree2) == 1


def functiontest(*args):
    pass


def mainTest(item):
    classtest(item)
    functiontest(item)

    print("All tests passed")



if __name__ == "__main__":
    mainTest("Starter")