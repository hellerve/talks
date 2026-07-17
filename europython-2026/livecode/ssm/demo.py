"""
a state-space model in recurrence and convolution.

the whole architecture is a linear recurrence over a hidden state:

    h_t = A h_{t-1} + B x_t        (state update)
    y_t = C h_t                    (readout)

that runs one step at a time, like an rnn. the same model is a
single convolution with a kernel built from the matrices:

    y = x * K,   K = (CB, CAB, CA^2 B, ...)

recurrent to run cheap, convolutional to train in parallel. the two views
MUST agree on every input. that equality is a useful test.
"""

import numpy as np

# scalar state-space model with one hidden dim for clarity

# recurrent, one step at a time
def run_recurrent(x, A, B, C):
    h = 0.0
    ys = []
    for xt in x:
        h = A * h + B * xt # h_t = A h_{t-1} + B x_t
        ys.append(C * h) # y_t = C h_t
    return np.array(ys)

# convolutional, unroll into one kernel
def make_kernel(A, B, C, length):
    # k_i = C A^i B
    # impulse response, unrolled recurrence
    return np.array([C * (A ** i) * B for i in range(length)])

def run_convolutional(x, A, B, C):
    K = make_kernel(A, B, C, len(x))
    y = np.zeros(len(x))
    for i in range(len(x)): # causal convolution y = x * K
        y[i] = np.dot(K[: i + 1][::-1], x[: i + 1])
    return y

# play the whole thing
if __name__ == "__main__":
    rng = np.random.default_rng(0)
    x = rng.standard_normal(12)
    A, B, C = 0.9, 0.5, 1.3 # |A| < 1 keeps the powers A^k stable

    y_rec = run_recurrent(x, A, B, C)
    y_conv = run_convolutional(x, A, B, C)

    assert np.allclose(y_rec, y_conv), "the two views must agree"

    print(f"sequence length    {len(x)}")
    print("parameters         A, B, C  (scalar SSM)")
    print(f"kernel  C A^i B    {np.array2string(make_kernel(A, B, C, 5), precision=3)} ...")
    print(f"recurrent  == convolutional   "
          f"(max diff {np.abs(y_rec - y_conv).max():.1e})")
    print("two schedules, one model: train as a convolution, run as a loop.")
