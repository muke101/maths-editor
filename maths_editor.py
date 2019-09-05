class Node():
    def __init__(self, key):
        self.key = key
        self.parent = None
        self.left = None
        self.right = None

    def hasChildren(self): 
        if self.left == None or self.right == None:
            return False
        return True

    def hasBaseLeaves(self):
        if self.hasChildren():
            for child in [self.left, self.right]:
                if child.hasChildren():
                    return False
            return True
        return False

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

class Term():
    def __init__(self, token):
        self.expodent = 1
        if token.isdigit():
            self.coeff = int(token)
            self.variable = None
        else:
            self.coeff = 1
            self.variable = token
    
    def printTerm(self):
        expodentStr = ''
        coeffStr = ''
        variableStr = ''

        if self.expodent != 1:
            expodentStr = '^'+str(self.expodent)
        if self.coeff != 1:
            coeffStr = str(self.coeff)
        if self.variable != None:
            variableStr = self.variable

        if expodentStr == '' and coeffStr == '' and variableStr == '':
            return '1'
        else:
            return expodentStr+coeffStr+variableStr

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
            stack.push(Term(token))

        else:
            node = Node(token)
            
            terms = [stack.pop(), stack.pop()]

            for c, term in enumerate(terms): #create node instances for lone numbers/variables
                if type(term) != Node:
                    terms[c] = Node(term) 
                terms[c].parent = node

            node.right = terms[0] #term being acted on goes on the right
            node.left = terms[1]
            stack.push(node)

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
        test = [[node.parent.key for node in children] for children in self.baseLeaves]
        self.evaluate()

    def findBaseLeaves(self, node):
        if node.hasBaseLeaves():
            self.baseLeaves.append([node.left, node.right])

        elif node.hasChildren():
            for child in [node.left, node.right]:
                self.findBaseLeaves(child)
    
    def evaluate(self):
        for children in self.baseLeaves:
            operation = children[0].parent.key
            print(operation)

    #def add(self, rightTerm, leftTerm):

    #def substract(self, rightTerm, leftTerm):

    #def multiply(self, rightTerm, leftTerm):

    #def divide(self, rightTerm, leftTerm):

    #def raise(self, rightTerm, leftTerm):

if __name__ == '__main__':
    equation = "a+b*(c^d-e)^(f+g*h)-i"
    postFixEquation = infixToPostFix(equation)
    tree = treeBuilder(postFixEquation)
    #printTree(tree)
    evaluator(tree)
