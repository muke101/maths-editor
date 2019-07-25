equation = "5x + 10"

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

for i in tokeniser(equation):
    print(i)
            
            

