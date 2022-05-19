import BinaryTree as b
import random


def classtest(item):
    """
    Test the BinaryTree class
    :param item:
    :return: None
    """
    tree = b.treeNode()
    assert b.is_empty(tree) == True
    assert b.is_leaf(tree) == True
    assert b.size(tree) == 0
    tree2 = b.treeNode()
    tree2.root = "a"
    assert b.is_empty(tree2) == False
    assert b.is_leaf(tree2) == True
    assert b.size(tree2) == 1
    assert b.is_exists(tree2, "a") == True
    assert b.is_exists(tree2, "b") == False


def functiontest(*args):
    tree = b.treeNode()
    randomlist = [random.randrange(1, 100, 1) for i in range(10)]
    print(randomlist)
    for item in randomlist:
        if b.is_exists(tree, item):
            print("{} is already in the tree".format(item))
            count = b.lookup(tree, item)
            b.insertIntoTree(tree, item, count + 1)
            assert b.lookup(tree, item) == count + 1
        else:
            b.insertIntoTree(tree, item, 1)


    b.printInOrder(tree)




def mainTest(item):

    classtest(item)
    functiontest(item)

    print("All tests passed")



if __name__ == "__main__":
    mainTest("Starter")