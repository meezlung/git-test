from dataclasses import dataclass

@dataclass
class Node:
    value: str
    prev: "Node | None" = None
    next: "Node | None" = None

class Queue:
    def __init__(self, size: int = 0, head: Node | None = None, tail: Node | None = None):
        self.size = size
        self.head = head
        self.tail = tail

    def enqueue(self, value: str):
        new_node = Node(value, prev=self.tail)
        if self.tail:
            self.tail.next = new_node

        return Queue(self.size + 1, 
                     head=self.head if self.head else new_node, 
                     tail=new_node)

    def dequeue(self):
        if self.size == 0 or self.head is None:
            return None
        new_head = self.head.next
        
        if new_head:
            new_head.prev = None
        
        return self.head.value, Queue(self.size - 1,
                                      head=new_head,
                                      tail=self.tail if new_head else None)
    
    def peek(self):
        return self.head.value if self.head else None
    
    def __len__(self):
        return self.size

class TippyMemory:
    def __init__(self):
        self.timestamps = [0]
        self.history: dict[int, Queue] = {0: Queue()}

        super().__init__()

    def _find_latest(self, t: int):
        left, right = 0, len(self.timestamps) - 1

        while left < right:
            mid = (left + right + 1) // 2
            if self.timestamps[mid] <= t:
                left = mid
            else:
                right = mid - 1
        
        return self.timestamps[left]

    def entered_line(self, t: int, customer: str) -> None:
        prev_t = self._find_latest(t)
        self.history[t] = self.history[prev_t].enqueue(customer)
        self.timestamps.append(t)

    def front_served(self, t: int) -> None:
        prev_t = self._find_latest(t)
        if len(self.history[prev_t]) > 0:
            new_queue = self.history[prev_t].dequeue()
            if new_queue is None:
                return None
            self.history[t] = new_queue[1]
            self.timestamps.append(t)

    def slept(self, t: int) -> None:
        idx = 0
        while idx < len(self.timestamps) and self.timestamps[idx] <= t:
            idx += 1
        self.timestamps = self.timestamps[:idx]
        self.history = {k: v for k, v in self.history.items() if k <= t}

    def front(self, t: int) -> str | None:
        prev_t = self._find_latest(t)
        return self.history[prev_t].peek()
