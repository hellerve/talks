"""
multi-scale modelling  skeleton (rgm-lite).

trimmed, runnable stand-in for a renormalizing generative model. the
real rgm is a generative model with a learned prior at each scale, here
we keep only the main idea and make it easy to see:

  - coarse-grain a signal down a pyramid (pool),
  - apply the *same* learned operator at every scale (weight sharing),
  - reconstruct fine from coarse (unpool),

so the renormalization loop is to coarse-grain, model, repeat with one
shared block, and it’s all we do. no "generative" here.
"""

import numpy as np

# down/up sampling:
def pool(x): # (N,) -> (N/2,), average pairs
    return x.reshape(-1, 2).mean(-1)

def unpool(x): # (N/2,) -> (N,), repeat each
    return np.repeat(x, 2)

# our shared operator, reused at every scale
def block(x, w): # a tiny learned smoother
    # circular 3-tap filter; `w` is the only parameter, shared across scales
    return w[0] * np.roll(x, 1) + w[1] * x + w[2] * np.roll(x, -1)

# the renormalization loop: down, model, back up
def multiscale(x, w, levels):
    # descend, coarse-graining as we go, remembering each scale
    pyramid = [x]
    for _ in range(levels):
        pyramid.append(pool(pyramid[-1]))

    # ascend: model the coarse level, then add detail back at each step
    coarse = block(pyramid[-1], w)
    for finer in reversed(pyramid[:-1]):
        up = unpool(coarse)
        detail = block(finer - up, w) # diff to the coarse level
        coarse = up + detail
    return coarse

# demo
if __name__ == "__main__":
    N, levels = 16, 3
    rng = np.random.default_rng(0)
    # a signal with a global trend (coarse) and local wiggles (fine)
    t = np.linspace(0, 1, N)
    x = np.sin(2 * np.pi * t) + 0.1 * rng.standard_normal(N)
    w = np.array([0.25, 0.5, 0.25]) # shared smoothing op

    y = multiscale(x, w, levels)

    assert y.shape == x.shape, "multi-scale must return to full resolution"
    print(f"signal length      {N}, pyramid levels {levels}")
    print(f"coarsest scale     {N >> levels} samples (global structure)")
    print(f"shared parameters  {w.size} weights, reused at every scale")
    print(f"shape preserved    {x.shape} -> {y.shape}")
    print(f"reconstruction err {np.abs(x - y).mean():.4f} "
          f"(detail kept across scales)")
