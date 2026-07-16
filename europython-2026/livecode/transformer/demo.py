"""
a transformer block in numpy.

one pre-norm transformer block (attention + mlp with residuals and layer
norm). point is not a trained model, it is to get the architecture: three
matmuls and a softmax for attention, an add for the residual connections,
and a handful of invariants that pin the whole thing down.

the punchline is `block`, the residual `+`, which is why deep stacks train at
all.
"""

import numpy as np

# softmax, scores into a distribution
def softmax(x):
    x = x - x.max(-1, keepdims=True) # subtract row max: no exp overflow
    e = np.exp(x)
    return e / e.sum(-1, keepdims=True) # each row sums to 1

# self-attention
def attention(x, Wq, Wk, Wv):
    # x: (T, d).  one head, no mask, to keep the idea naked.
    Q = x @ Wq # (T, d)
    K = x @ Wk # (T, d)
    V = x @ Wv # (T, d)
    d_k = Q.shape[-1]
    scores = Q @ K.T / np.sqrt(d_k) # (T, T): token-to-token weight
    return softmax(scores) @ V # (T, d): weighted mix of values

# layer norm is plumbing
def layer_norm(x, gamma, beta, eps=1e-5):
    mu = x.mean(-1, keepdims=True) # per token, over features
    var = x.var(-1, keepdims=True)
    return gamma * (x - mu) / np.sqrt(var + eps) + beta

# a 2-layer mlp
def mlp(x, W1, b1, W2, b2):
    h = np.maximum(0.0, x @ W1 + b1) # relu
    return h @ W2 + b2

# the block reads the stream and writes a correction back
def block(x, p):
    x = x + attention(layer_norm(x, p["g1"], p["b1"]),
                      p["Wq"], p["Wk"], p["Wv"]) # the residual +
    x = x + mlp(layer_norm(x, p["g2"], p["b2"]),
                p["W1"], p["mb1"], p["W2"], p["mb2"])
    return x

# random weights, just to exercise
def init(d, hidden, seed=0):
    rng = np.random.default_rng(seed)
    def s(*shape):
        return rng.standard_normal(shape) * 0.02
    return {
        "Wq": s(d, d), "Wk": s(d, d), "Wv": s(d, d),
        "g1": np.ones(d), "b1": np.zeros(d),
        "g2": np.ones(d), "b2": np.zeros(d),
        "W1": s(d, hidden), "mb1": np.zeros(hidden),
        "W2": s(hidden, d), "mb2": np.zeros(d),
    }

# tests
def checks():
    T, d, hidden = 5, 8, 32
    x = np.random.default_rng(1).standard_normal((T, d))
    p = init(d, hidden)

    # attention rows are a probability distribution
    Q = x @ p["Wq"]
    K = x @ p["Wk"]
    w = softmax(Q @ K.T / np.sqrt(d))
    assert np.allclose(w.sum(-1), 1.0), "attention rows must sum to 1"

    # layer norm zeroes mean and unit-scales variance (before g, b)
    n = layer_norm(x, np.ones(d), np.zeros(d))
    assert np.allclose(n.mean(-1), 0.0, atol=1e-6), "ln mean must be 0"
    assert np.allclose(n.var(-1), 1.0, atol=1e-3), "ln var must be 1"

    # shapes in equal shapes out
    y = block(x, p)
    assert y.shape == x.shape, f"block changed shape: {x.shape} -> {y.shape}"

    print("all invariants hold:")
    print(f"  attention rows sum to 1      (max err "
          f"{abs(w.sum(-1) - 1).max():.1e})")
    print(f"  layer norm mean 0, var 1     "
          f"(|mean| {abs(n.mean(-1)).max():.1e}, "
          f"var {n.var(-1).mean():.3f})")
    print(f"  block preserves shape        {x.shape} -> {y.shape}")

if __name__ == "__main__":
    checks()
