# do we really need this, sleep on it!
# doesnt the list implementation cover all these basic functionalities?

class Stack:
    def __init__(self):
        self.stack = []

    def push(self, x):
        self.stack.append(x)

    def pop(self):
        if not self.empty():
            self.stack.pop()

    def top(self):
        if self.empty():
            return None

        return self.stack[-1]

    def empty(self):
        return not self.stack

    def size(self):
        return len(self.stack)