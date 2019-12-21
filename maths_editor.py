from sympy import *

class Node:
    def __init__(self, key):
        self.key = key
        self.parent = None
        self.left = None
        self.right = None

    def hasChildren(self): 
        if self.left == None or self.right == None:
            return False
        return True

    def hasBaseLeaves(self): #a node with 'base leaves' as I'm referring to them is simply a node who's children are both leaves. This is required to know where to begin with evaluation.
        if self.hasChildren():
            for child in [self.left, self.right]:
                if child.hasChildren():
                    return False
            return True
        return False

class operandStack:
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

class Term:
    def __init__(self, token):
        self.exp = 1
        if token.isdigit():
            self.coeff = int(token)
            self.var = None
        else:
            self.coeff = 1
            self.var = token
    
    def printTerm(self):
        expodentStr = ''
        coeffStr = ''
        variableStr = ''

        if self.expo != 1:
            expodentStr = '^'+str(self.expo)
        if self.coeff != 1:
            coeffStr = str(self.coeff)
        if self.var != None:
            variableStr = self.var

        if expodentStr == '' and coeffStr == '' and variableStr == '':
            return '1'
        else:
            return expodentStr+coeffStr+variableStr

class conTerm:
    def __init__(self, term):
        self.numerator = term 
        self.expodent = 1
        self.denominator = 1 #this could be a potentially procarious choice. I'm hoping that not including division and powers in the expression list but rather as seperate variables will make simplification of term combining easier (ie, combining two terms that share common demoniators) as parsing the expression list won't be required. It feels like one of those things that'll come back to bite later down the line though, or at the very least not straightforward.
        self.terms = [term]

    def addTerm(self, term, operator):
        self.terms.append(term)

class tokeniser:
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
        if token.isdigit():
            stack.push(Node(token))

        elif token.isalpha():
            stack.push(Node(symbols(token)))

        else:
            parent = Node(token)
            
            terms = [stack.pop(), stack.pop()]

            for c, term in enumerate(terms): #create node instances for lone numbers/variables
                terms[c].parent = parent

            parent.right = terms[0] #term being acted on goes on the right
            parent.left = terms[1]
            stack.push(parent)

    return stack.pop() #stack should be collasped down to one root node

def printTree(root):
  thislevel = [root]
  while thislevel:
    nextlevel = list()
    for n in thislevel:
      if type(n.key) != Term:
        print(n.key)
      else:
        print (n.key.printTerm())
      if n.left: nextlevel.append(n.left)
      if n.right: nextlevel.append(n.right)
    print()
    thislevel = nextlevel

class evaluator:
    def __init__(self, root):
        self.precedence = {'-': 1, '+': 1, '*': 2, '/': 2, '^': 3}
        self.baseLeaves = []
        self.findBaseLeaves(root)
        self.traverse()

    def findBaseLeaves(self, node):
        if node.hasBaseLeaves():
            self.baseLeaves.append([node.left, node.right])

        elif node.hasChildren():
            for child in [node.left, node.right]:
                self.findBaseLeaves(child)
    
    def traverse(self):
        for children in self.baseLeaves:
            left = children[0]
            right = children[1]
            parent = self.evaluate(left, right)

            parent = parent.parent

            while parent.hasBaseLeaves():
                parent = self.evaluate(parent.left, parent.right)
                if parent.parent is None:
                    return parent
                parent = parent.parent

    def evaluate(self, left, right):

        parent = left.parent
        operation = parent.key

        if operation == '+':
            parent.key = self.add(left.key, right.key)
        elif operation == '-':
            parent.key = self.subtract(left.key, right.key)
        elif operation == '*':
            parent.key = self.multiply(left.key, right.key)
        elif operation == '/':
            parent.key = self.divide(left.key, right.key)
        elif operation == '^':
            parent.key = self.raiseTo(left.key, right.key)
                                                                               
        parent.left = None
        parent.right = None

        return parent

    def add(self, left, right):
        return left + right 

    def subtract(self, left, right):
        return self.add(left, -1*right)

    def multiply(self, left, right):
        return left * right

    def divide(self, left, right):
        return self.multiply(left, self.raiseTo(right, -1))

    def raiseTo(self, left, right):
        return left**right

if __name__ == '__main__':
    equation = "a+b*(c^d-e)^(f+g*h)-i"
    postFixEquation = infixToPostFix(equation)
    tree = treeBuilder(postFixEquation)
    evaluator(tree)
    print(tree.key)
