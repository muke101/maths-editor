# maths editor
A terminal based editor for mathematical equations that exists to make writing and operating on maths as easy on the keyboard as it is on paper.
Type up your equations (with keybinds to make it easier) and then use another set of keybinds in a different mode (not unlike vim) to maniuplate 
the equation in real time, keeping a log of previous changes you can jump between. Not intended to solve equations like wolframalpha, you still
do all the working, but now you can do this working on a terminal, instead of with paper and pen.
Intended for use in physics, so of course algebra, trig and calculus will all be implemented, intending to use symengine for the complicated calculus stuff though.


My general and loosly connected notes on how I expect this program will eventually work:


edit mode and operation mode
in edit mode, just straight up go in and change equatoin at will, perhaps with helpful keybinds for symbols
in operation mode, key binds that carry out operations on the equation, like 'minus 5' or 'divide by x'. 
operation mode follows mathematical rules, edit mode doesn't.

In operation mode, equation is parsed and then represented into a parse tree, with each component having the operation acted on it
parse tree is transvered upward as it's evaluated.

Backend works as follows:
Tokeniser -> stack to convert from infix to postfix -> parse tree constructed from postfix notation -> evaluation using different types/objects for each term

Tree
tree is constructed in a regular, recurssive fashion. 
Reads off operator stack
1. creates node under current node (or creates root) for currnet read operator
2. pulls one operand off operand stack and sets it as left child
3. reads another operator off operator stack and sets it as right child
4. repeat until operator stack is empty, after which last remaining operand is used for last right child
As such, for operators where order matters (minus, division), the left child is always the operand that is being operated on (left child minus right child)

Evaluation
The evaluation is done through type checking. Every element broken down to it's single state (ie the leaves of the tree)
has it's own type, can be either variable (x is a unique type, y is a unique type) or a number (10 is the same type as 5)
when evaluating expressions, either regular decimal operations take place (10/5) or objects must be used to determine if and how
different variable types can combine. Encountering y*x would return a new type yx. If this were then added with xy, type checks would
yield that this can legally go to 2xy, which is still the same type but now with a modified coefficient (which doesn't change it's fundemental type).
xy*xy however would yield xy^2, which is a new type. 
Hazy on how the type evaluation is gonna be done, but expectng to basically be abusing OOP.

Types
there exist types and metatypes. Types are class objects that hold basic information about the single term - variable (x, y, xy), coeffcient and power.
When types are compared, they go through these values for both to check for compatibility. So xy^-1 and xy would first check variables, and determine they're the same,
and then check powers, and as they differ, they would be deemed different types, and could not be added or subtracted into one term with a new coefficient, 
Metatypes are types that contain more types. They don't exist in the final products of evaluation but are needed as intermediate products.
For instance take x^2+x+5 multipled by 2. This would be broken up at the plus operators, then further into it's component terms, after which 2 would be multiplied to each
term indivisually. As this transverses back up the parse tree it returns the result to be operated on with the other original term, so
2x^2 would find itseld being compared to one other term for addition, instead of two terms like they really are. These two terms are held in the metatype which acts as 
the single term 2x^2 is compared against, and is essencially just (2x+10). The indivisual terms exist as objects themselves, and they are refernced to within the metatype object.
So, the metatype is iterated over for every term that it holds and compared indivisually against 2x^2. In this case, neither can be cleanly added, and we already know they can't be added to eachother
as they were already compared against to create the metatype. The metatype is for the purposes of the tree one thing, but it can hold as many indivisual types that have previously been evaluted
within it. Metatypes can as such be compared to other metatypes, and I guess the only way to do that would be with n*m complexity, as every term would have to be compared to every other term in the opposing metatype.

