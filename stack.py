class Stack:
    """
    Реализация стека на базе вектора
    (для языка Python она тривиальна)
    """

    def __init__(self):
        self.array = []

    def push(self, c):
        self.array.append(c)

    def pop(self):
        return self.array.pop()

    def top(self):
        return self.array[len(self.array) - 1]

    def is_empty(self):
        """
        Просто проверка на пустой стэк
        """
        return len(self.array) == 0
