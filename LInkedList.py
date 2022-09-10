
class Node:
    def __init__(self, data):
        self.data = data
        self.next = None

def get_position(head, position):
    current = head
    for i in range(position):
        current = current.next
    return current

def insert_node(head, position, data):
    current = head
    for i in range(position - 1):
        current = current.next
    new_node = Node(data)
    new_node.next = current.next
    current.next = new_node
    return head

def print_list(head):
    current = head
    while current:
        print(current.data)
        current = current.next

def delete_node(head, position):
    current = head
    for i in range(position - 1):
        current = current.next
    current.next = current.next.next
    return head


def createlinkedlist():
    head = Node(1)
    tail = head
    for i in range(2, 10):
        tail.next = Node(i)
        tail = tail.next
    return head




asda = createlinkedlist()
print_list(asda)
print("\n")
asda = insert_node(asda, 3, 10)
print_list(asda)
print("\n")
asda = delete_node(asda, 3)
print_list(asda)




