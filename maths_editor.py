equation = "a+b*(c^d-e)^(f+g*h)-i"


class Node():
    def __init__(self, key):
        self.key = key
        self.left = None
        self.right = None

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

def infixToPostFix(equation): 
    precedence = {'-': 1, '+': 1, '*': 2, '/': 2, '^': 3} #I don't understand why it's this and not BIDMAS but it works 
    postFix = []
    stack = operandStack()
    for char in tokeniser(equation).tokens():
        if char.isdigit() or char.isalpha(): #is operand
               postFix.append(char)
        elif char == '(':
            stack.push(char)
        elif char == ')':
            op = stack.pop()
            postFix.append(op)
            while  stack.peek() != '(':
                op = stack.pop()
                postFix.append(op)
            stack.pop()
        elif stack.isEmpty() or stack.peek() == '(' or precedence[stack.peek()] < precedence[char]:
            stack.push(char) 
        elif stack.peek() != '(' and precedence[stack.peek()] >= precedence[char]:
            op = stack.pop()
            postFix.append(op)
            while not stack.isEmpty() and stack.peek() != '(' and  precedence[op] >= precedence[char]: 
                op = stack.pop()
                postFix.append(op)
            if op != '(':
                stack.push(char)  
    while not stack.isEmpty():
        postFix.append(stack.pop())

    return postFix

def treeBuilder(postFixEquation):
    stack = operandStack()

    for token in postFixEquation:
        if token.isdigit() or token.isalpha():
            stack.push(token)

        else:
            node = Node(token)
            
            terms = [stack.pop(), stack.pop()]

            for c, term in enumerate(terms): #create node instances for lone numbers/variables
                if type(term) != type:
                    nodeChild = Node(term)
                    terms[c] = nodeChild 
                    
            node.right = terms[0] #term being acted on goes on the right
            node.left = terms[1]
            stack.push(node)
        
