# learning by building small models

## why tiny models?

**you (probably) have already used one**
- everyone here has used an llm, a translator, or good code completion.
- underneath each is a neural network: arrays of numbers and a few matmuls.
- i always tend to think to myself "i want to build one" if i want to understand
  something, so here we are.

**frameworks are for production code**
- open pytorch to learn attention and you wade through kernels, autograd, device placement.
- that machinery exists to be fast and general, not to be read.
- for learning we go the other way, namely minimal and small. maximize
  understanding and concepts.
- if you want to learn about infra and optimization, frameworks are a good
  resource.

**the practice**
- build a small runnable version yourself.
- in python and numpy, small enough to read top to bottom and understand it.
- the real constraint is to hold the whole thing in your head.

**what you trade**
- you gain: every value visible, a wrong number has one source, shapes explain the design.
- you give up: scale, throughput, benchmark numbers. the models just aren’t very good, but they
  don’t need to be
- optimise for understanding, nothing else.

**the setup**
- we only need numpy arrays, a loop, a plot.
- shape-first: treat an array program as its shapes.
- the greek in papers is shorthand for this array code. if you’re new to this or
  math scares you, listen to my words. if you’re comfortable with math or ml,
  look at the slides. we have two tracks here.
- also: we’ll be using some fancy words. feel free to start throwing them around
  in conversation for smartness points, but don’t get scared by them. they’re
  just words, and you can substitute or understand them.

## a tiny transformer, end to end

the architecture that makes the world go round: since "attention is all you need", this is the
thing.

**what a transformer computes**
- on a mechanical level: the transformer takes in tokens, makes their embeddings
  (a vector), then runs an attention and an mlp layer over it (n times,
  depending on the model’s depth), and produces output.
- the whole job of a transformer: give each word a vector that captures its meaning
  in *this* sentence, because the same word means different things in different contexts.
- each layer every word looks at all the others and updates itself (attention), then
  is reshaped on its own (the mlp). more rounds, richer vectors.
- a real model is this same round stacked around a hundred times, just wider.

**self-attention**
- "the trophy didn't fit in the case because it was too big." representing "it" means
  finding "trophy", and which word matters changes with the sentence, so the mixing can't
  be fixed wiring, it has to be chosen from the content. that is why attention exists.
  it’s a fuzzy problem, and fuzzy problems can be learned in weights.
- each position turns its embedding into three vectors: a query (what it wants to find),
  a key (what it contains, so others can find it), and a value (what it passes on when
  matched). the relevance of one position to another is their query · key.
- it is a fuzzy dict lookup: `d[key]` returns one value for one input. attention compares
  your query against every key and returns a blend of all the values, weighted by
  relevance.
- if query and key were the same vector, attention would be symmetric: A attending to B would
  force B to attend to A just as much. but reference is directional ("it" needs "trophy", not
  the reverse), so query and key are separate matrices, which lets the score from i to j differ
  from j to i.
- √dk just keeps the scores a sane size: the dot product sums over dk terms, so without it the
  scores grow with the vector length and softmax collapses onto a single word instead of
  blending. mechanics, not idea.

**softmax**
- what it's for: we have raw relevance scores, any numbers, some negative, and we need weights
  we can average with, positive and summing to one. softmax is the standard way to get there.
- pure plumbing, very standard.
- why exponentiate rather than just clamp and divide: exp makes everything positive and turns
  a gap in scores into a ratio in the weights, so a slightly higher score wins a lot more weight.
  a soft pick, mostly the top but it keeps some of the rest.
- the overflow fix is not a hack: exp explodes for big scores, so subtract the row's max first.
  shifting every score by the same amount cancels out, so the weights are identical and nothing
  overflows. neat, right?

**residual connections**
- the problem: to train, a correction signal is pushed back through every layer, and each layer multiplies it by some small factor. a hundred small factors multiplied together is basically zero, so the bottom layers get no signal and never learn. this is what stopped people stacking deep networks before 2015.
- why adding is the fix: with x + f(x) the input passes through untouched alongside the change, so each layer's factor becomes "one plus a little" instead of "a little". one times one times one, a hundred times, is still about one, so the signal rides the +'s all the way down without collapsing. addition is what turns the vanishing multipliers into ~1. (resnets, 2015.)

**layer normalization**
- the problem: the numbers in each vector come out at wildly different scales through the layers, one tiny, the next enormous, and that instability wrecks training.
- what the fix does: grab each vector, subtract its average, then shrink or stretch it to a fixed size. whatever goes in, a same-scale vector comes out.
- the honest part: why this exact rescale is what helps isn't derivable, it's an empirical normalization hack that happens to work. even people who've trained models mostly take it on faith. (ml aside: it's feature standardization, between every layer.)

**let's build one** (live cue)
```
def attention(x, Wq, Wk, Wv):
    Q = x @ Wq
    K = x @ Wk
    V = x @ Wv
    d_k = Q.shape[-1]
    scores = Q @ K.T / np.sqrt(d_k)
    return softmax(scores) @ V

def layer_norm(x, gamma, beta, eps=1e-5):
    mu = x.mean(-1, keepdims=True)
    var = x.var(-1, keepdims=True)
    return gamma * (x - mu) / np.sqrt(var + eps) + beta

def block(x, p):
    x = x + attention(layer_norm(x, p["g1"], p["b1"]),
                      p["Wq"], p["Wk"], p["Wv"])
    x = x + mlp(layer_norm(x, p["g2"], p["b2"]),
                p["W1"], p["mb1"], p["W2"], p["mb2"])
    return x
```

**a transformer block**
- that was about sixty lines, no framework.
- the model behind the chatbot is this block, wider and deeper. just stack it
  and use a bunch of data of questionable provenance to train it.
- the matrices get bigger, but the operations do not change.

## paper to prototype

**read an equation as an array program**
- every symbol is an array, every subscript an axis.
- a sum over an index is a matmul or a .sum(axis=...).
- write the shapes in a comment before the code.
- if the shapes compose, you usually understood the mechanics formula.
  understanding their meaning is different, but requires a different skillset.
  no amount of array math will get you there.

**catch bugs early with boring things**
- assert shapes at every boundary so it fails at the line that caused it.
- unit-test the math: one input where you worked out the answer by hand.
- the overfit test: memorise ten examples. if you cannot, it is broken, and
  you don’t need to try a bigger case.

## multi-scale modelling (rgm)

**structure across scales**
- an image has structure at every zoom level: overall composition, then objects,
  then texture, then pixels. a model that only ever works at full resolution has
  to learn all of it at once, which is hard and expensive.
- so this architecture works coarse-to-fine: get the big picture on a shrunken
  version first, cheaply, then add detail as you zoom back in. a genuinely different
  shape of model from the transformer.

**coarse to fine**
- the operations are ones you know from images: downsampling is making a thumbnail
  (average a block of pixels into one), upsampling is blowing it back up. stack them
  and you get the same signal at a ladder of resolutions.
- every shrink throws information away, and every blow-up has to invent detail back.
  this is where the modelling has to happen.

**renormalization**
- why reuse the very same weights at every level: it hinges on the assumption that the
  same kinds of patterns show up at every zoom level. an edge looks like an edge
  whether you're near or far. when that roughly holds, one small operator does the work
  of many, at no extra parameter cost.
- the name is borrowed from theoretical physics: in the renormalization group you zoom
  out of a system step by step and the same rules keep describing it. that's the
  analogy where "renormalization" comes from.

**generativity**
- generative means the model produces new data, new images say, instead of labelling or
  transforming data you hand it.
- rgm also runs the pyramid backwards: start from a coarse, blurry sample, and at each
  scale a learned model adds the next level of detail, until you have a full image.
  reusing structure across scales keeps that tractable.
- my toy has the multi-scale skeleton, the pyramid and the shared operator, but not the
  generative part or the learned coarse-graining. it shows the shape of the idea, not the
  finished model. i have a bigger example on my blog where we actually have
  generativity, but that is a bit bigger than what we’ll cover here.

## state-space models

**attention has a cost problem**
- attention's power is that every position sees every other, but that also explodes:
  the work grows with the square of the length. a thousand tokens is a million
  comparisons, a hundred thousand is ten billion. that is why long context is hard and
  expensive.
- state-space models are one way around it: they read the sequence in a single linear
  pass, so cost grows with length, not length squared. that is what lets people run them
  on audio, dna, or a whole book with a fraction of the funding.

**a state-space model**
- it's an accumulator loop: walk the sequence, keep a running state, update it each step,
  except the state is a vector and the update is a matrix multiply. that’s all.
- every step is linear, no relu or tanh in the loop like an rnn has. it looks like a
  limitation, but it actually lets the same model also be written as a convolution.

**one model with two forms**
- because the loop is linear, you can rewrite it as one convolution, a single fixed
  filter slid over the whole sequence, computing exactly the same thing.
- in practice you train with the convolution (the whole sequence in parallel on a gpu,
  and it’s fast) and run with the loop (one step at a time, tiny memory). you almost
  never get fast training and cheap inference from one set of weights. that’s why they’re
  so exciting! but there is another thing.

**attention also has a memory problem**
- to generate each new token, attention needs the key and value of every earlier token,
  held in a cache. that cache grows with the length of the context, so a long conversation
  or document means keeping all of it in memory, and it only ever gets bigger. it is one of
  the annoyances of running transformers on long inputs.
- a lot of harnesses also persist memory in markdown or other files and silently
  inject them into the context, which works, but is clunky, unprincipled, and
  it’s unclear whether it’s actually accurate.

**constant memory**
- an ssm never keeps the past tokens. the hidden state is a fixed-size vector that summarises
  everything so far, and to produce the next output you only need that state, not the history.
  so memory doesn't grow with length: you can stream a whole book or an hour of audio through
  it while holding one small state.
- the tradeoff is that a fixed budget is lossy compression of the past, and squeezing long
  history into it well is what some of the newer approaches are about, and what we skip. look
  at mamba or hybrid architectures if you want to find out more!
- but! because the state is a small fixed object, you can save it, reload it, even fork it. a
  conversation's memory becomes a first-class thing you own and pass around. a transformer has
  no comparable handle: its memory is the conversation itself.

## your own tiny model lab

let’s take a step back and see waht we learned from looking at these three
archictectures, and think about how you could replicate this at home.

**a reusable harness**
- the three models were completely different, but everything around them was identical.
- so the reusable thing is the harness: a dataset small enough to overfit, a forward pass with
  shapes asserted, invariants as tests, build tooling, math helpers. write it once and any new
  architecture drops in. a relu or a softmax stay around.

**when to stop**
- the toy is for understanding.
- when you need scale or speed, move to pytorch or jax.
- the difference is you now know what the framework is doing under the hood.
  kind of.

**the takeaway**
- a paper is a specification.
- the fastest way to understand one is to implement the smallest version that runs.
- pick the thing that scared you most and do it.

## likely questions

- *does it train?* it is a forward pass; add an optimiser and it trains on a toy task. today was the architecture.
- *why numpy, not pytorch?* precisely to keep autograd and kernels out of view. pytorch is the right tool once you understand what it hides.
- *are these the real architectures?* faithful skeletons. each "what's missing" slide names what the real version adds.
- *where do i start?* pick an intimidating paper and overfit ten examples of its smallest case.
