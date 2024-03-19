from node import Node


class CircularList:
    def __init__(self):
        self.head = None

    def is_empty(self):
        return self.head is None

    def insert_element(self, dato):
        new_node = Node(dato)
        if self.is_empty():
            self.head = new_node
            new_node.next = self.head

        else:
            current = self.head
            while current.next != self.head:
                current = current.next
            current.next = new_node
            new_node.next = self.head

    def get_list(self):
        if self.is_empty():
            return []

        result = []
        current = self.head
        while True:
            result.append(current.data)
            current = current.next
            if current == self.head:
                break
        return result

    def delete_element(self, data):
        if self.is_empty():
            print('The list is empty')
            return

        if self.head.data == data:
            current = self.head
            while current.next != self.head:
                current = current.next
            if self.head == self.head.next:
                self.head = None
            else:
                current.next = self.head.next
                self.head = self.head.next
        else:
            current = self.head
            prev = None
            while True:
                if current.data == data:
                    prev = current.next
                    break
                prev = current
                current = current.next
                if current == self.head:
                    break

    def delete_all(self):
        if self.is_empty():
            print('The list is already empty')
            return

        current = self.head
        while current.next != self.head:
            temp = current.next
            del current
            current = temp
        del current
        self.head = None

    def search_element(self, data):
        if self.is_empty():
            print('The list is empty')
            return

        current = self.head
        while True:
            if current.data == data:
                print('The element {data} has been found')
                return True
            current = current.next
            if current == self.head:
                print(f'The element {data} has been found')
                return True

    def edit_element(self, search_data, new_data):
        if self.is_empty():
            print('The list is empty')
            return
        current = self.head
        while True:
            if current.data == search_data:
                current.data = new_data
                return
            current = current.next
            if current == self.head:
                print(f'The element {search_data} has been not found')
                return
