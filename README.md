# maths editor

# overview:
A terminal based editor using ncurses for mathematical equations that exists to make writing and operating on maths as easy on the keyboard as it is on paper.
Type up your equations (with keybinds to make it easier) and then use another set of keybinds in a different mode (not unlike vim) to maniuplate 
the equation in real time, keeping a log of previous changes you can jump between. Not intended to solve equations like wolframalpha, you still
do all the working, but now you can do this working on a terminal, instead of with paper and pen.
Intended for use in physics, so of course algebra, trig and calculus will all be implemented, intending to use symengine for the calculus evaluation though (I'm not insane!)

# General notes on how each component does/will work:

For the technical details on how the workings, I have a blog post that's being updated as new progress gets made on the project, so please check that out if you're interested: https://1337haxing.blogspot.com/2019/09/research-and-architecture-ideas-for.html

This is a rough outline of how the program itself should ideally work as a finished product:

Edit mode and operation mode:
in edit mode, just straight up go in and change equatoin at will, perhaps with helpful keybinds for symbols
in operation mode, key binds that carry out operations on the equation, like 'minus 5' or 'divide by x'. 
operation mode follows mathematical rules, edit mode doesn't.
In operation mode, equation is parsed and then represented into a parse tree, with each component having the operation acted on it

Frontend interface:
Built in ncurses, users of course switch between the two modes to write then maniuplate equations as needed. Main section is dedicated of course for the equation being worked on but also a growing history of previous iterations of the equation after each operation. This allows the potential for users to scroll back in their history to before they carried out certain operations, and even use vim-like versioning where you can create new branches of the history for different operations. This would be hard to implement, but so powerful that it would be worth it. 

Directly selection of subsections of the expression for manipulation would be a requirment, similar to how you move around an expression on a scientific calculator. For example, wanting to factor one side of a plus sign but not the other. This'll be very difficult to implement as it'll require constant parsing of the expression around where the operators are, but hopefully doable. Bracketting at every opportunity, even if brackets are hidden to the user, should make it a lot easier. 

There should also be different work spaces avalible for use that you can switch between and then work on multiple equations at once, and even set an equation from one workspace as the new subject of another equation, assuming the variables match up for the substitution (ie, they both equal the same thing).


