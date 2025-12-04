# Prakruthi Praveen
# Builds a Doubly Linked List that can update, insert, or remove nodes


class DLLNode:
    def __init__(self, data):
        self.data = data
        self.prev = None
        self.next = None


class DoublyLinkedList:
    def __init__(self):
        self.head = None
        self.tail = None
        self.size = 0

    # --------- Inserts ---------
    def insert_at_begin(self, data):
        new_node = DLLNode(data)
        if self.head is None:
            self.head = new_node
            self.tail = new_node
        else:
            new_node.next = self.head
            self.head.prev = new_node
            self.head = new_node
        self.size += 1

    def insert_at_index(self, data, index):
        if int(index) < 0 or int(index) > self.size:
            raise IndexError("Index out of range")
        if int(index) == 0:
            self.insert_at_begin(data)
            return
        if int(index) == self.size:
            self.insert_at_end(data)
            return
        new_node = DLLNode(data)
        current = self.head
        for i in range(index - 1):
            current = current.next
        new_node.next = current.next
        new_node.prev = current
        current.next.prev = new_node
        current.next = new_node
        self.size += 1

    def insert_at_end(self, data):
        new_node = DLLNode(data)
        if self.tail is None:
            self.head = new_node
            self.tail = new_node
        else:
            self.tail.next = new_node
            new_node.prev = self.tail
            self.tail = new_node
        self.size += 1


    # --------- Deletions ---------
    def remove_first_node(self):
        if self.head is None:
            return None
        if self.head == self.tail:
            self.head = None
            self.tail = None
        else:
            self.head = self.head.next
            self.head.prev = None
        self.size -= 1

    def remove_last_node(self):
        if self.tail is None:
            return
        if self.head == self.tail:
            self.head = None
            self.tail = None
        else:
            self.tail = self.tail.prev
            self.tail.next = None
        self.size -= 1

    def remove_at_index(self, index):
        if int(index) < 0 or index > self.size:
            raise IndexError("Index out of range")
        if int(index) == 0:
            self.remove_first_node()
            return
        if int(index) == self.size:
            self.remove_last_node()
            return
        current = self.head
        for i in range(index):
            current = current.next
        current.prev.next = current.next
        current.next.prev = current.prev
        self.size -= 1

    def remove_node(self, data):
        current = self.head
        while current is not None:
            if current.data == data:
                if current == self.head:
                    self.remove_first_node()
                    current = self.head
                    continue
                if current == self.tail:
                    self.remove_last_node()
                    current = None
                    continue
                next_node = current.next
                current.prev.next = current.next
                current.next.prev = current.prev
                self.size -= 1
                current = next_node
                continue
            current = current.next

    # --------- Checks ---------
    def size_of_DLL(self):
        return self.size

    # --------- Print functions ---------
    def print_DLL(self):
        current = self.head
        while current is not None:
            print(current.data, end=" <-> ")
            current = current.next
        print("None")

    def rev_print_DLL(self):
        current = self.tail
        while current is not None:
            print(current.data, end=" <-> ")
            current = current.prev
        print("None")

    def update_node(self, data, index):
        if index < 0 or index >= self.size:
            raise IndexError("Index out of range")
        current = self.head
        for i in range(index):
            current = current.next
        current.data = data


def main():
    # create a new linked list
    dllist = DoublyLinkedList()

    # add nodes to the linked list
    dllist.insert_at_end('a')
    dllist.insert_at_end('b')
    dllist.insert_at_begin('c')
    dllist.insert_at_end('d')
    dllist.insert_at_index('x', 4)
    dllist.insert_at_index('z', 4)
    dllist.insert_at_index('g', 2)

    # print the doubly linked list
    print("Node Data:")
    dllist.print_DLL()

    # print the doubly linked list in reverse
    print("Reverse Node Data:")
    dllist.rev_print_DLL()

    print("\nSize of linked list:", dllist.size_of_DLL())

    # remove nodes from the linked list
    print("\nAfter Removing First Node:")
    dllist.remove_first_node()
    dllist.print_DLL()

    print("\nAfter Removing Last Node:")
    dllist.remove_last_node()
    dllist.print_DLL()

    print("\nAfter Removing Node at Index 1:")
    dllist.remove_at_index(1)
    dllist.print_DLL()

    print("\nAfter Removing Node at Index 2:")
    dllist.remove_at_index(2)
    dllist.print_DLL()

    print("\nUpdate node Value to 'z' at Index 0:")
    dllist.update_node('z', 0)
    dllist.print_DLL()

    print("\nSize of linked list:", dllist.size_of_DLL())

    print("\nAttempt to Remove Node with data 'g':")
    dllist.remove_node('g')
    dllist.print_DLL()

    print("\nAfter Removing Node with data 'z':")
    dllist.remove_node('z')
    dllist.print_DLL()


if __name__ == "__main__":
    main()

