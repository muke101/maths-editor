equation = "5x + 10 - 5"


class tokeniser():
    def __init__(self,equation):
        self.equation = equation
        self.bracketPairs = 0
        self.length = len(equation)
        self.inNumber = False
        self.number = []

    def getChar(self, char): #helper function to contain all the special case characters that need to alter counters etc
        if  char == ' ':
            return ''
        elif char == '(':
            self.bracketPairs+=1
            return '('
        elif char == ')':
            self.bracketPairs-=1
            return ')'
        else:
            return char

    def tokens(self):
        for c, char in enumerate(self.equation, 1):
            if c == 1 and char != '(':
                yield '('
                self.bracketPairs+=1

            if char.isdigit():
               if not self.inNumber:
                   self.inNumber = True
               self.number.append(char)
            elif self.inNumber and not char.isdigit():
                self.inNumber = False
                yield ''.join(self.number) #yield full number when first non-digit char is seen
                self.number = []
                if char.isalpha(): #include implicit multiplication
                    yield '*'
                yield self.getChar(char)
            else:
                yield self.getChar(char)
             
            if c == self.length: #I wish python used null terminators..
                if self.inNumber:
                    yield ''.join(self.number)
                if self.bracketPairs > 0:
                    yield ')'

class operandStack():
    def __init__(self):
        self.precedence = {'-': 1, '+': 2, '*': 3, '/': 4, '^': 5}
        self.stack = []

    def isEmpty(self):
        return len(self.stack) == 0

    def push(self, op):
        self.stack.append(op)

    def pop(self):
        return self.stack.pop() if self.isEmpty() else None 

    def peek(self):
        return self.stack[-1]
 


class node():
    def __init__(self, key):
        self.key = key
        self.left = None
        self.right = None

    def insert(self, key):
        if self.left == None:
            self.left = key
        elif self.right == None:
            self.right = key
        else:
            raise ValueError('node full')
