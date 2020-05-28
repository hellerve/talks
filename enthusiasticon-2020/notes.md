Hey! I’m Veit, and today I want to talk about hammers and nails.

Most of us have probably heard the old saying "If all you have is a hammer,
everything looks like a nail”. It’s one of the many polite ways in which
we’re telling our peers that they are doing something wrong.

The sentence didn’t actually originate in Computer Science, though. It is
often referred to as “Maslow’s Law” or “Maslow’s Hammer”, paying tribute to
a psychologist who codified that law in an article in the 60s, but it is
probably much older than that. My cursory search for its origin pointed at
least to the 19th century, but it’s probably even older than that.

And we use it a bit as a truism, as something to avoid any argument. A phrase
intended to burn the battleground of thought, once and for all, if you will
entertain my pathos for a second.

And I keep coming back to that phrase, because I usually hate generalizations.
All our tools, be it languages or frameworks or interfaces, impose some form of
order on our day-to-day existence as technologists. Some lenses are just more
focused than others.

And so the question we need to ask ourselves is: is it always bad to submit
fully to that lens?

And in my quest to get a satisfying answer to this question I at some point
remembered another overused quote that shapes our thought, at least in certain
circles.

It is by Alan Perlis, of Algol and Turing Award fame, and it reads like this:
“It is better to have 100 functions operate on one data structure than 10
functions on 10 data structures”. It’s historically been one of those phrases
that slightly eccentric Lisp people used to rationalize the spartan aesthetic
of their programming environments.

But these days most of us don’t use “one data structure”. We use heaps and
queues and lists and stacks and trees and hashmaps and Hash-Array Mapped
Semi-Tries with orange peels and crushed ice.

So let’s ask ourselves: what do we get if we try to make everything one data
structure? I’m going to pick four languages that went down that route, more or
less adhering to it, and I’m going to show some of their affordances.

The first one I’m going to talk about is the one I’m most familiar with: Lisp.
Lisp stands for “List Processing”. And the proof is in the pudding. Everything
in Lisp is a list, even the syntax!

Let’s look at an example—this uses more-or-less Clojure, because I wanted it to
be concise. For those of you who don’t know Lisp, everything in parentheses is
a list. So the definition, building a macro here, is a list as well!

And this particular macro takes a bunch of arguments, and builds another list.
And that list will end up looking like an if statement, or rather, it will be
an if statement. And thus the macro and is just a representation of logical
conjunction, expressed in terms of if. And we work on the syntax the same way
we work on data.

Let’s go to the language I’m second most familiar with: SmallTalk. SmallTalk is
the grandfather of object-oriented languages, but it’s a very active
grandfather, still around and telling the kids to stay of his lawn so that he
can enjoy the piece and quiet of a good development environment.

And, SmallTalk contends, in a good object-oriented language EVERYTHING should
be an object. There are no primitives. There is no control flow. You get
objects.

And so in SmallTalk, True is a subclass of Boolean, and so is False. And both
of them implement a function called ifTrue:ifFalse: that takes two blocks, kind
of like callbacks. And True will call the trueBlock, and False will call
the falseBlock, and anything doing any sort of logic will return either of those
classes that you can send this message to. And everything just sort of works
out okay.

At this point I should probably mention that it’s fine not to understand the
code examples. Let them wash over you.

Let’s look at two languages I’m less familiar with: Forth and APL.

Forth works on stacks. Everything is put on a stack, and all the operator
operate on the things on that stack, and everything happens from left to right,
always.

My Forth example actually implements comments. Comments start with an opening
parenthesis and close with a closing parenthesis. The function for comments is
thus just opening parenthesis. It puts the closing parenthesis on the stack,
and then just collects everything until it finds that (that’s what word does),
and then drops the parenthesis again, ignoring all the input. It is an
“immediate” word which basically means that it should be run as soon as it is
seen in the code by the compiler, comparable to what a macro would do in other
languages. And thus implementing comments is as simple as telling the compiler
to jump ahead.

Let’s go to APL, because I’m running out of time. APL stands for “A Programming
Language”, but I always imagine it to stand for “Array Programming Language”.
APL and its descendants (there is a whole family, like for all languages that I
mention in this talk) mostly operate on n-dimensional arrays. Everything is an
operation on an array, and this, too, leads to idiosyncratic solutions.

APL also has a somewhat infamous fetish for unique glyphs, and I couldn’t get
LaTEX to render my code example, so I decided to type them into a REPL and take
a screenshot. I apologize.

I actually brought two examples. Everything behind this little round figure
with two legs is a comment, so this is the first and only example in this talk
for documented code. The first program sums the numbers from 1 to 15 by
building an array, and then reducing over it using addition. In APL, you
usually read the program from right to left, barring any comments. The second
example is a little more tricky. It’s the outer product of the numbers from one
to ten with themselves, which is a fancy way to say that it’s all the
combinations of the numbers from one to ten. The first three glyphs implement
the outer product part, the judgemental emoticon in the middle says to use the
argument to its right twice to the thing on its left, and then we take the
numbers from one to ten.

Now this has been a tour de force of four completely and utterly anachronistic
languages, but the main question that you might have right now is “So what?”.

I mean, this is all cool, and the examples that I showed might have made you go
“huh, this is really clever”. But does it really do anything for us? What do we
gain by giving up the comfort of something more expressive, more general? And
I’m not naming names here, every language is a beautiful flower.

I like to think that thinking that uses less axioms is more learnable. The less
base things I need to know, the better. And it answers a lot of questions. How
do I do anything in Lisp, in Forth, in APL? I use a list, a stack, an array. I
encourage you to read “It’s not what programming languages do, it’s what they
shepherd you to” by Jussi Pakkanen.

But the other side of the equation is that you have a lot of new questions to
answer that you didn’t have to answer before. How do I talk to the filesystem
if everything is an array? In what way is a graphics stack an object?

But I think that there is a quality here that is liberating, a breath of fresh
air in a world that is all too often concerned with what we already do day to
day. Constraints can be liberating instead of, well, constraining. This is
purely anecdotal, but I found to be highly productive in SmallTalk and Lisp,
because I could just pop open any piece of machinery, no matter how deep in my
stack, and understand it, because it speaks the same language that I speak,
fifteen layers of abstraction later. There is something to be said for using
the same tools everywhere; it leads to a certain uniformity, charm, and
creativity that I personally miss otherwise.

And so, in conclusion, if I am asked to use a hammer, I’m fully prepared to
make the world my nail.

Thank you.
