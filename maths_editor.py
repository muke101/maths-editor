equation = "5x + 10 + 5"

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

class tokeniser():
    def __init__(self,equation):
        self.equation = equation.replace(' ','')
        self.bracketPairs = 0
        self.length = len(self.equation)
        self.inNumber = False
        self.number = []

    def getChar(self, char):
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
                yield ''.join(self.number)
                self.number = []
                if char.isalpha():
                    yield '*'
                yield self.getChar(char)
            else:
                yield self.getChar(char)
             
            if c == self.length:
                if self.inNumber:
                    yield ''.join(self.number)
                if self.bracketPairs > 0:
                    yield ')'

for i in tokeniser(equation).tokens():
    print(i)
 
#construct tree with beautiful recurssion

