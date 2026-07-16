# AI Architecture Katas: Learning by Building Small Models in Plain Python

45-minute slot.

Deep learning is often taught through large frameworks and large models,
which is great for getting real projects out of the door, but not always
great for learning. This talk is about a different practice: building
tiny, runnable versions of various modern architectures with minimal
dependencies (mostly Python and NumPy) to learn about the ideas through
application.

We'll get our feet wet by building a small Transformer end-to-end and
learn about the model architecture that started the craze. Then we switch
perspectives, and learn about other architectures, always staying small
and nimble, focusing on applying the math and breathing life into
formulas. We will look at multi-scale modelling (in a simplified version
of Renormalizing Generative Models), State Spaces, and other scary
concepts, until they are not scary at all anymore.

You'll leave with a model for turning papers into little prototypes that
stay true to ideas and the starting point for your own little lab to build
models yourself.

Prerequisites: a basic understanding of NumPy and a willingness to look at
Greek letters. No deep learning framework knowledge required.

## Outline

- **0–4 min: Why tiny models?**
  - What you gain (visibility, debuggability, intuition), what we do not
    prioritize (scale, performance).
  - Setup: mostly NumPy, shape-first thinking, minimal scaffolding.
- **4–15 min: A tiny Transformer end-to-end**
  - Attention as shape algebra (Q/K/V, scores, softmax stability).
  - Residual stream and layer norm (plumbing that matters).
  - Quick sanity checks: invariants + tiny tests.
- **18–23 min: Paper to prototype workflow**
  - Reading equations as array programs.
  - Shape discipline, unit tests for math, and small evals to catch bugs
    early.
  - Notebook to module path to capture our experiments.
- **23–33 min: Multi-scale modelling (RGM-lite)**
  - Coarse to fine operators (down/up or pooling/unpooling analogues).
  - A renormalization-style loop: reuse the same structure across scales.
  - What it teaches you and what's missing.
- **33–38 min: State-space models, made un-scary**
  - Core recurrence + convolutional view.
  - Where the speed/expressivity comes from at a conceptual level.
  - A tiny implementation sketch + what to test.
- **38–40 min: Wrap-up, building your own "tiny model lab"**
  - A reusable template: data, model, loss, tests, visualization hooks.
  - When to stop and move to PyTorch/JAX.
- **40–45 min: Q&A** (or spillover if I get carried away).
