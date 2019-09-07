# maths editor

# overview:
A terminal based editor using ncurses for mathematical equations that exists to make writing and operating on maths as easy on the keyboard as it is on paper.
Type up your equations (with keybinds to make it easier) and then use another set of keybinds in a different mode (not unlike vim) to maniuplate 
the equation in real time, keeping a log of previous changes you can jump between. Not intended to solve equations like wolframalpha, you still
do all the working, but now you can do this working on a terminal, instead of with paper and pen.
Intended for use in physics, so of course algebra, trig and calculus will all be implemented, intending to use symengine for the calculus evaluation though (I'm not insane!)

# General notes on how each component does/will work:

Edit mode and operation mode:
in edit mode, just straight up go in and change equatoin at will, perhaps with helpful keybinds for symbols
in operation mode, key binds that carry out operations on the equation, like 'minus 5' or 'divide by x'. 
operation mode follows mathematical rules, edit mode doesn't.
In operation mode, equation is parsed and then represented into a parse tree, with each component having the operation acted on it

Frontend interface should roughtly be like this:
Built in ncurses, users of course switch between the two modes to write then maniuplate equations as needed. Main section is dedicated of course for the equation being worked on but also a growing history of previous iterations of the equation after each operation. This allows the potential for users to scroll back in their history to before they carried out certain operations, and even use vim-like versioning where you can create new branches of the history for different operations. This would be hard to implement, but so powerful that it would be worth it. 

Directly selection of subsections of the expression for manipulation would be a requirment, similar to how you move around an expression on a scientific calculator. For example, wanting to factor one side of a plus sign but not the other. This'll be very difficult to implement as it'll require constant parsing of the expression around where the operators are, but hopefully doable. 

There should also be different work spaces avalible for use that you can switch between and then work on multiple equations at once, and even set an equation from one workspace as the new subject of another equation, assuming the variables match up for the substitution (ie, they both equal the same thing).

Backend works as follows:
Tokeniser -> stack to convert from infix to postfix -> parse tree constructed from postfix notation -> evaluation using different types/objects for each term

Parse Tree
The parse tree is constructed very simply thanks for the postfix notation. Operands are added to a stack as they're scanned, operators pop two operands off the stack and create a new node with the operator as the parent and the operands as the children, then the resulting node is pushed back onto the stack. As it's back on the stack, node objects can then be popped off again to be added as children to new nodes constructed from newly scanned operators. The result is that by the end of the expression, what remains on the stack is just the root node of the fully constructed parse tree.

Evaluation
The evaluation is done through type checking. Every element broken down to it's single state (ie the leaves of the tree)
has it's own type, can be either variable (x is a unique type, y is a unique type) or a number (10 is the same type as 5)
when evaluating expressions, either regular decimal operations take place (10/5) or objects must be used to determine if and how
different variable types can combine. Encountering yx would return a new type yx. If this were then added with xy, type checks would
yield that this can legally go to 2xy, which is still the same type but now with a modified coefficient (which doesn't change it's fundemental type).
xyxy however would yield xy^2, which is a new type. 

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
within it. Metatypes can as such be compared to other metatypes, and I guess the only way to do that would be with n by m complexity, as every term would have to be compared to every other term in the opposing metatype.

