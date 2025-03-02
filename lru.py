
class Node:
    """ Nodo de la lista doblemente enlazada """
    def __init__(self, key, value):
        self.key = key
        self.value = value
        self.usage_count = 0
        self.prev = None
        self.next = None

class DoublyLinkedList:
    """ Lista doblemente enlazada para gestionar la caché LRU """
    def __init__(self):
        self.head = Node(None, None)
        self.tail = Node(None, None)
        self.head.next = self.tail
        self.tail.prev = self.head

    def add_to_end(self, node):
        node.prev = self.tail.prev
        node.next = self.tail
        self.tail.prev.next = node
        self.tail.prev = node

    def remove(self, node):
        node.prev.next = node.next
        node.next.prev = node.prev

    def move_to_end(self, node):
        self.remove(node)
        self.add_to_end(node)

    def remove_least_recently_used(self):
        lru_node = self.head.next
        self.remove(lru_node)
        return lru_node

class LRUCache:
    """ Caché LRU optimizada con contador de uso """
    def __init__(self, capacity: int):
        self.capacity = capacity
        self.cache = {}
        self.dll = DoublyLinkedList()

    def get(self, key: str):
        if key not in self.cache:
            return None
        node = self.cache[key]
        node.usage_count += 1 
        self.dll.move_to_end(node)
        return node.value

    def put(self, key: str, value: str):
        if key in self.cache:
            node = self.cache[key]
            node.usage_count += 1
            node.value = value
            self.dll.move_to_end(node)
        else:
            if len(self.cache) >= self.capacity:
                lru_node = self.dll.remove_least_recently_used()
                del self.cache[lru_node.key]
            new_node = Node(key, value)
            self.dll.add_to_end(new_node)
            self.cache[key] = new_node

    def get_recent_colors(self):
        colors = []
        node = self.dll.tail.prev
        while node != self.dll.head:
            colors.append((node.value, node.usage_count))
            node = node.prev
        return colors

    def set_capacity(self, new_capacity):
        self.capacity = new_capacity
        while len(self.cache) > self.capacity:
            lru_node = self.dll.remove_least_recently_used()
            del self.cache[lru_node.key]

