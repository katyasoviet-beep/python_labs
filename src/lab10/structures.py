from collections import deque
from typing import Any, Optional


class Stack:
    def __init__(self):
        self._data: list[Any] = []

    def push(self, item: Any) -> None:
        self._data.append(item)

    def pop(self) -> Any:
        if self.is_empty():
            raise IndexError("Stack is empty")
        return self._data.pop()

    def peek(self) -> Optional[Any]:
        if self.is_empty():
            return None
        return self._data[-1]

    def is_empty(self) -> bool:
        return len(self._data) == 0

    def __len__(self) -> int:
        return len(self._data)


class Queue:
    def __init__(self):
        self._data: deque[Any] = deque()  

    def enqueue(self, item: Any) -> None:
        self._data.append(item) 

    def dequeue(self) -> Any:
        if self.is_empty():
            raise IndexError("Queue is empty")
        return self._data.popleft()

    def peek(self) -> Optional[Any]:
        if self.is_empty():
            return None
        return self._data[0]

    def is_empty(self) -> bool:
        return len(self._data) == 0

    def __len__(self) -> int:
        return len(self._data)  


if __name__ == "__main__":
    print("=== Демонстрация Stack ===")
    
    # Пример использования Stack
    stack = Stack()
    
    print("1. Добавляем элементы в стек:")
    stack.push(1)
    stack.push(2)
    stack.push(3)
    print(f"   Размер стека: {len(stack)}")
    print(f"   Верхний элемент (peek): {stack.peek()}")
    
    print("\n2. Извлекаем элементы :")
    while not stack.is_empty():
        item = stack.pop()
        print(f"   Извлечён: {item}, осталось: {len(stack)}")
    
    print("\n3. Проверка пустого стека:")
    print(f"   Стек пуст: {stack.is_empty()}")
    print(f"   Peek пустого стека: {stack.peek()}")
    
    try:
        stack.pop()
    except IndexError as e:
        print(f"   ✅ Поймали ошибку: {e}")
    
    print("\n" + "="*50)
    print("=== Демонстрация Queue ===")
    
    # Пример использования Queue
    queue = Queue()
    
    print("1. Добавляем элементы в очередь:")
    queue.enqueue("A")
    queue.enqueue("B")
    queue.enqueue("C")
    print(f"   Размер очереди: {len(queue)}")
    print(f"   Первый элемент (peek): {queue.peek()}")
    
    print("\n2. Извлекаем элементы (FIFO):")
    while not queue.is_empty():
        item = queue.dequeue()
        print(f"   Извлечён: {item}, осталось: {len(queue)}")
    
    print("\n3. Проверка пустой очереди:")
    print(f"   Очередь пуста: {queue.is_empty()}")
    print(f"   Peek пустой очереди: {queue.peek()}")
    
    try:
        queue.dequeue()
    except IndexError as e:
        print(f"   ✅ Поймали ошибку: {e}")
    
    print("\n" + "="*50)
 
    
    