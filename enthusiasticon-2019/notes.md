Hello everyone! I’m Veit, and this talk is about abstractions or, more
specifically, about abstractions in philosophy.

Let me start by introducing my agenda. First, we’re going to talk about my
motivation, then about one book, then about another book, and finally we’re
going to revisit my motivations and summarize. Alright? Let’s go!

I’m going to start with a disclaimer—this talk has a lot of disclaimers. This
one deals with the branch of philosophy that we talk most about when we talk
about technology and philosophy: technophilosophy. Think Ray Kurzweil, AI
ethics, that sort of stuff. That’s all very interesting, but not what I want to
talk about today.

Instead, I want to focus on the fact that we always build abstractions. We
always build abstractions, no matter whether we build an API, render an image,
or write a network driver.

Philosophers also always build abstractions, although they deal with a different
set of things. They build abstractions for ideas such as cognition, self,
identity, all that jazz. But abstractions they build, and they have been doing
so for a few thousand years at least. What I want to do today is shine a few
spotlights on some ideas from some philosophers that might be interesting for
you, and hopefully whet your appetite for more.

The first objection that might come to your mind is that you haven’t studied
philosophy, and neither have I—and English isn’t my first language. But the
beauty about philosophy is that it deals with very simple things: cognition,
self, identity, all those things you can relate to and have an immediate idea
of. You might not always understand what people are saying about these things,
but at their core, they’re very close to you.

With that out of the way, let’s look at the first book.

And here I’m going to present my second disclaimer: this book isn’t actually
about what I want to talk about. Instead it’s about episteme, which are
basically those assumptions that we build our worldviews and knowledge on
without knowing that we do. This doesn’t make any sense without context, and I’m
not concerned with that today. Instead, what I want to talk about is the
introduction, where he talks a little bit about order, classifications, and
abstractions.

Foucault starts his introduction with a quote by Jorge Luis Borges: [read
quote]. And this is an obviously absurd classification, but it begs the
question: why is it absurd?

I would argue it’s absurd in the same way that this is absurd. For those of you
who don’t know what they’re looking at, this is a traceback, where first call
... And what I would argue is that Borges’ classification and this one are
flawed in the same way, because you can obtain, acquire and get an access token,
and it’s all the same thing, and in the same vein an animal can both “belong to
the emperor” and be “embalmed”.

So what defines classifications is the space between them, not their label. What
I mean by that is that a good abstraction separates things very clearly from
one another. You have one thing with a bunch of functionality here, and then
a very different thing with a very different set of functions over there, and
neither the things nor their functionality should overlap.

And why would I even classify? Well, what’s neat about classifications is that
if they are good and sensible, they lead to better abstractions. If I know where
to look for stuff, I will find it earlier, like on a well organized bookself.

It’s also important to note that whenever you abstract, you build a
classification, whether you meant to or not. By even just rearranging things,
their context and their meaning changes.

At the end of this section I want to talk about an important caveat though:
never assume that your abstractions are _the_ way to view the world. Order
always imposes hierarchy, and it’s easy to get sucked into that. But no
hierarchy will ever tell you the whole story. There are obviously flawed ways
to rank humans, for instance, like race, and then there are more heinously
flawed things that at a first glance might make sense, like IQ or even
intelligence itself, were it measurable. All your classifications impose
hierarchy, and that’s not always good.

Now I want to talk about the second book, which is Zen and the Art of
Motorocycle Maintenance by Robter Pirsig. It’s a very good book, about a
motorcycle trip of a father and a son, a life changed by mental illness, and
his notion of “Quality”.

Quality is the thing that exists for isntance between the observer and the
observed of a painting. If I look at the Mona Lisa, I assign qualities to it,
and in the same vein when I look at Cubism I assign a different set of
qualities to it. And what’s especially interesting is that he maintains that
these qualities only exist in the relationship, meaning that the qualities that
I see are not the ones that you see and vice versa.

What this means is that abstractions can never be objective. There is always
context, always a use case. This is very important to keep in mind whenevery
you’re building abstractions. They’re never perfect, no matter how hard you
try.

So the question we have to ask ourselves then is: how do bring objectivity
back, or at least accomodate users with a different set of ideas? And at this
point I want to bring up the only technical thing in this talk: Git.

Git is the ultimate leaky abstraction.

What I mean by that is that in Git you have both control over what they call
the porcelain, which is all the high-level functionality that Git exposes, and
the plumbing, which are the low-level functions that they wouldn’t need to
expose necessarily. This gives very advanced users a way to control even the
way commits are built and other things like that.

I guess the question we just answered is whether abstractions have to hide their
details, and I’d argue that that only works if you consider your abstractions
to be good enough for everyone, which they never are.

So, in summary:

Thinking about abstractions will help you articulate your aesthetics and
standards and help figure out whether you’re doing a good job adhering to them.

If nothing else, reading philosophy will either inspire you, or at least build
your vocabulary to articulate what your ideals are, which is useful in its own
right.

I want to finish up with a personal guidebook on how to write better
abstractions. [...]

I also have a commentated reading list, but sadly I don’t have time to go
through it anymore. Instead I’ll refer you to my talks repository, where you
can find these slides, and we can talk about any and all things and any and all
of the books I mentioned afterwards.

Thank you.


