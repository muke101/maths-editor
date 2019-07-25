equation = "5x + 10"

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

def tokeniser(equation):
    inNumber = False
    number = []
    length = len(equation)
    
    for c, char in enumerate(equation, 1):
        if char.isdigit():
            if not inNumber:
                inNumber = True
            number.append(char)
        elif inNumber and not char.isdigit():
            inNumber = False
            yield ''.join(number)
            number = []
            yield char
        elif char == ' ':
            continue
        else:
            yield char
        if c == length:
            if inNumber:
                yield ''.join(number)
            else:
                yield char

 
#construct tree with beautiful recurssion

