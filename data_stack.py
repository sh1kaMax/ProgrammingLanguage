from exceptions import StackOverflowError, StackUnderflowError


class Stack:
    stack = None
    max_size = None

    def __init__(self, max_size):
        self.stack = []
        self.max_size = max_size

    def push(self, arg):
        if len(self.stack) == self.max_size:
            raise StackOverflowError(self.max_size)
        if arg is not None:
            self.stack.append(arg)

    def pop(self):
        if len(self.stack) == 0:
            return None
        value = self.stack[-1]
        self.stack.pop()
        return value
