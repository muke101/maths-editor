equation = "5x + 10 - 5"


class tokeniser():
    def __init__(self,equation):
        self.equation = equation.replace(' ', '')
        self.bracketPairs = 0
        self.length = len(self.equation)
        self.inNumber = False
        self.number = []

    def getChar(self, char): #helper function to contain all the special case characters that need to alter counters etc
        if char == '(':
            self.bracketPairs+=1
            return '('
        elif char == ')':
            self.bracketPairs-=1
            return ')'
        else:
            return char

    def tokens(self):
        for c, char in enumerate(self.equation, 1):

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
             
            if c == self.length: #I wish python had null terminators..
                if self.inNumber:
                    yield ''.join(self.number)
                if self.bracketPairs > 0:
                    yield ')'

class operandStack():
    def __init__(self):
        self.stack = []

    def isEmpty(self):
        return True if len(self.stack) == 0 else False

    def push(self, op):
        self.stack.append(op)

    def pop(self):
        return self.stack.pop() if not self.isEmpty() else None 

    def peek(self):
        return self.stack[-1]

def infixToPostFix(equation): 
    precedence = {'-': 1, '+': 2, '*': 3, '/': 4, '^': 5}
    postFix = []
    stack = operandStack()
    for char in tokeniser(equation).tokens():

        if char.isdigit() or char.isalpha(): #is operand
               postFix.append(char)
        elif stack.isEmpty() or stack.peek() == '(' or precedence[stack.peek()] < precedence[char]:
            stack.push(char) 
        elif stack.peek() != '(' and precedence[stack.peek()] > precedence[char]:
            op = stack.pop()
            postFix.append(op)
            while not stack.isEmpty() and precedence[op] >= precedence[char]:
                op = stack.pop()
                if op == '(':
                    stack.push(char)
                    break
                else:
                    postFix.append(op)
            if op != '(':
                stack.push(char)  
        elif char == '(':
            stack.push(char)
        elif char == ')':
            op = stack.pop()
            postFix.append(op)
            while op != '(':
                op = stack.pop()
                postFix.append(op)
            stack.pop()
    while not stack.isEmpty():
        postFix.append(stack.pop())

    return postFix

print(infixToPostFix(equation))


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
