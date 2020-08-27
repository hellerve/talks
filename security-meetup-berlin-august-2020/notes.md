Hi I'm Veit and today I want to talk about memory safety issues in memory safe
languages.

There are many ways in which supposedly memory safe languages may not live up to
their potential. In this talk I will mostly focus on issues within the
constraints of the language rather than talking about their compiler or
interpreter environments. This is because they usually are written in
memory unsafe languages like C or C++. They are subject to the same bugs that
you find in any other C code base. Just consider Python, which has had 49 CVEs
assigned to it in the last 12 years, 13 of which were overflow-related. Or think
of the various JavaScript runtimes and how people keep crafting exploits to
break out of their sandboxing mechanisms, whether it’s through fooling the
JIT’s range analysis or through simple bugs in the implementation of
primitives.

We will talk about runtimes, though, because sometimes the devil is in an
execution environment that we didn’t even really know was there, or didn’t
consider when thinking about threats.

While talking about this it will seem as if I am bashing on what might be your
favorite programming language. I'm not doing that because I think that language
or in fact any of the languages that I talk about are bad but because I think it
is important to realize that there are no silver bullets. There are good
approaches but in the end you will always be able to shoot yourself in the foot
and it is important to know how that happens. Whenever I use a specific language,
I use it because it illustrates an underlying idea, nothing more, and nothing
less.

One more thing before I start: I will cast a quick highlight on a few things,
hoping that this will lead to heightened sensibilities when thinking about
these things. If you tune out for a problem here and there, no worries! It
probably doesn’t concern you. And if it does, and you still weren’t listening,
I reserve the right to a hearty "told-ya-so".

Let's start with denial of service or DOS bugs. DOS bugs can happen in a variety
of ways and today I want to talk about those kinds of DOS bugs that you might
encounter in the wild. To drive the point home, I will talk about real problems
that exist in your language today. If your language is Go or Haskell.

My first example concerns the Go programming language, but not really. What I
actually want to talk about is concurrency, and Go happens to be one of the
languages that make concurrency extremely easy, and thus it’s easier to get it
wrong.

In Go, channels are the main abstraction for communicating between threads—or,
rather, Goroutines, which are Go’s notion of concurrent processes. Think of
mailboxes in Erlang, or queues in microservice architectures. Channels are
easy to construct, and easy to work with: you request one, give it to the
processes, and then you can read from them and write to them! Sadly, this leads
to a tendency to forget about them. We forget to read from them, leading to
memory leaks—because we  can’t free them! We forget to write a finalizer
message to our channel or to close it, and that leads to goroutine leaks...
And so on, and so on.

Remember, when concurrency is involved, you want to make sure you know about
the lifetimes of your processes. You want to know how and when they start,
and how and when they die. Basically, our model should account for anything
but solar flares and power outages, and if it doesn’t, you should know that
that is so.

Next up, staying with DoS bugs and Go—and this time being a bit more specific—, I
want to talk about a bug related to maps, a very foundational key value data
structure of the language. In issue number 20135 the developer reports that a
map will never shrink, i.e. it will always take up as much memory as it did when
it was at its biggest and the only way to shrink it again is to get rid of it
entirely, copying its contents to a new map. I brought an example program, but
I’m not sure how useful it is. If you want me to go through the program with
you, you can ask me during Q&A. Now, this is a very specific
problem, and it will likely only ever be a problem if you have many maps that
might grow to a certain size and then shrink again. That memory will never be
freed, and eventually, we run out of memory. The issue has been discovered in
2017, and it is still open. If you know about it you know how to mitigate it
(just make a new map and copy the entries), but currently there is no way to
know about it unless you either run into it yourself or thrawl through the
5916 open issues on the GitHub issue tracker—honestly, who does that before
writing their web application in Go?

What is the take-away here? There are a few: firstly, memory bugs do not need to
lead to corruption to cause problems. Secondly, if you have a runtime, some
things are out of your control, and you have to pray that the core developers
get things right. Shoutouts go out to Erlang, where the developers actively
tried breaking their map implementation with generative testing, leading to a
more robust implementation. I’ll link to a series of blog posts at the end. Go
check them out, especially if you’re not already convinced that property-based
testing and QuickCheck are awesome, or you want to learn more (or the first
thing) about hash-array-mapped tries.

Similar things can happen in Haskell—this is going to be an extremely technical
bit of this talk, but humor me for a second. Haskell is a lazy language. This
means that a value is only computed when it’s needed for the first time. This
makes profiling Haskell applications relatively hard, but comes with a unique
set of benefits that I have no time to get into, because they’re a big reason
some people choose Haskell over other ML-like functional languages. What I do
have to explain is that to achieve this, we need a basic building block called
a “thunk”, which is basically an unrealized value, a computation that still
needs to happen. It can be big or small, but it needs to be passed around the
runtime as-is until someone requests for it to be evaluated. Let’s see this in
action.

Here we have a binding for two variables, one being arithmetic—that’s what `x`
is—, and one blowing up—that’s what `error` is for, which is bound to `y`. But
in the body of the binding we only use `x`, and `y` is never needed, so it
works fine. In thunks this looks like this: you have a thunk here, it’s the
computation, unevaluated, and it’s sitting right here. And then you have a
thunk over there, which is the bad thunk. Then we request the value of `x`,
because we want to print it in our console, for instance, and this thunk, and
only this one, gets evaluated.

It’s all pretty complicated, and it gets even weirder when garbage collection
is concerned. For those of you in the
room who have some experience with virtual machines and garbage collection, you
might want to check out the Haskell model: it’s fantastically complicated
because of this, and because, in contrast to other VMs like the JVM, it
basically doesn’t use stack frames and does most of its work on the heap. This
also means that for short-lived variables inside a computation we spend time in
the garbage collector rather than the runtime, which might make it seems as if
the garbage collector is very slow, which it isn’t. The real problem is when we
don’t realize these thunks, because we keep adding small costs to the heap. It’s
not an inherent problem in the runtime, but it will make your program more
susceptible to space leaks, especially if STM—their concurrency model—is
involved. I don’t want to dive too deeply into this but I’ll leave you with some
papers that are very illuminating here in the end. What I do want to make clear
is that this can lead to a similar class of bugs as in Go, where our program
runs out of memory without actually needing all of it, and that, again, one of
our sad conclusions is that concurrency makes everything harder. And I want to
leave you with a quote by Neil Mitchell, because I found it to be very apt:
"Pinpointing space leaks is a skill that takes practice and perseverance.
Better tools could significantly simplify the process." And, as things always
go, these better tools never really arrived, because noone cares about program
correctness, not even Haskellers. The paper I quoted from is from 2013. Here’s
how Neil Mitchell operates now: "Using the benchmark I observed a space leak.
But the program is huge, and manual code inspection usually needs a 10 line
code fragment to have a change. So I started modifying the program to do less,
and continued until the program did as little as it could, but still leaked
space. After I fixed a space leak, I zoomed out and saw if the space leak
persisted, and then had another go." Does that sound awfully manual? It does to
me. This is from a blog post from this year. If someone wants to make Haskell
security much better, please write tooling for us!

Anyway, what’s the take-away here? If you have a runtime, you have to know it
to hunt down your bugs. And it’s another level of complexity if your runtime is
very complex.

But let’s move away from DOS bugs for now, and let’s talk about
honest-to-god memory corruption bugs. To do that, we have to move away from the
class of languages that use runtimes and garbage collection, because if they’re
implemented properly—which they never are because we’re all human—they eliminate
this class of bugs. You shouldn’t even be able to touch memory anywhere.

So let’s talk about Rust. I can already feel the inner tension of those of you
who are very fond of Rust and want to jump to defend it. Rust is great, just
like Haskell and Go are, but it comes with its own shortcomings. The most
dangerous bugs usually involve the `unsafe` keyword in some capacity or another,
like this silly example which will make your program bite the dust, and I would
argue that you should forbid unsafe code using
`#![forbid(unsafe_code)]` whenever possible, to avoid ending up in an advisory
on rustsec.org (on there, we find all the fun bugs that you find in C as well:
use after free, undefined behavior, doubles frees, unknown memory reads). But
there are other problems in Rust as well. In 2018, someone audited a lot of
popular Rust crates. They came to the conclusion that “If you want to write
DoS-critical code in Rust and use some existing libraries, you’re out of luck.
Nobody cares about denial of service attacks. You can poke popular crates with a
fuzzer and get lots of those. When you report them, they do not get fixed.”
That’s pretty damning in my book. They also found a few fun unsafe bugs, and I
encourage you to read the blog post if you’re unfamiliar with it.

In May, a bunch of Chinese researchers from universities and Baidu security also
came together to look at various issues in Rust code, to discover patterns.
“Most importantly, we find while Rust successfully limits memory-safety risks to
the realm of unsafe code, it also brings some side effects that cause new
patterns of dangling-pointer issues. In particular, most of the use-after-free
and double-free bugs are related to the automatic destruction mechanism
associated with the ownership-based memory management scheme”. Oof. Basically
the authors tell you that if you do anything that requires you to do memory
things manually, tell the compiler as early as possible and do bounds checking
as early as possible, or weird shit might happen. They also had some ideas for
increasing the checks inside unsafe regions in the compiler, which I
whole-heartedly stand behind.

So, what’s the take-away here? If your language has an escape hatch of any
form—we talked about Rust and unsafe here, but anything that turns off your
guarantees, like an unchecked memory view or byte array, might lead to trouble—,
then refrain from using it. Seriously, don’t use it. I know you think you know
what you’re doing. I think I know what I’m doing all the time, but I never do.
And neither do you. And if you have to use it, fuzz it, run property-based
testing on it, run all the semantic analyzers you can find on it, and then write
a proof for it, like they are doing in the RustBelt project.

Alright, I could probably stand here for another hour and tell you about all the
things that go wrong, until we’ve gone through every language in use today, and
have seen that all developers are fallible. But we don’t have to, because I
think you got my point already. Instead, I want to talk about something a bit
more positive.

Memory safety is always hard, no matter whether you do memory management by
hand, at runtime using garbage collection, or at compile time using something
like borrow checking or a substructural type system more generally. Each of
these approaches come with their own classes of bugs, and eliminate others. What
you have to do is make a choice, and stay informed about the system you are
working with. Many of the problems we looked at today are perfectly avoidable if
you know about them. Will avoiding them lead to perfectly safe systems then? Of
course not. But will you be able to sleep more soundly if you know that your
back is turned to the wall, and the door is locked? I hope so.

Thank you very much, and I will take any and all questions, especially
challenging ones.  If you’re feeling particularly antagonistic or contrarian
today, hit me with it.
