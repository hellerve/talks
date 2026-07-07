"""
refinement types.

base types carry a predicate that values must satisfy, and a call
typechecks when the caller's refinement implies the callee's.

real systems (liquid haskell, f*, dafny) discharge that implication with
an smt solver. this toy uses interval arithmetic over one integer
variable, which is enough to show that subtyping by
logical entailment, not by name.
"""

from dataclasses import dataclass
from typing import Union

INF = float("inf")


# predicates over the implicit variable `v`

@dataclass(frozen=True)
class TT: # always true
    pass


@dataclass(frozen=True)
class FF: # always false
    pass


@dataclass(frozen=True)
class GT: # v > n
    n: int


@dataclass(frozen=True)
class GE: # v >= n
    n: int


@dataclass(frozen=True)
class LT: # v < n
    n: int


@dataclass(frozen=True)
class LE: # v <= n
    n: int


@dataclass(frozen=True)
class EQ: # v == n
    n: int


@dataclass(frozen=True)
class NE: # v != n
    n: int


@dataclass(frozen=True)
class And:
    a: "Pred"
    b: "Pred"


@dataclass(frozen=True)
class Or:
    a: "Pred"
    b: "Pred"


Pred = Union[TT, FF, GT, GE, LT, LE, EQ, NE, And, Or]


# interpret predicates as unions of closed integer intervals

def to_set(p: Pred) -> list[tuple]:
    match p:
        case TT():
            return [(-INF, INF)]
        case FF():
            return []
        case GT(n):
            return [(n + 1, INF)]
        case GE(n):
            return [(n, INF)]
        case LT(n):
            return [(-INF, n - 1)]
        case LE(n):
            return [(-INF, n)]
        case EQ(n):
            return [(n, n)]
        case NE(n):
            return union([(-INF, n - 1)], [(n + 1, INF)])
        case And(a, b):
            return intersect(to_set(a), to_set(b))
        case Or(a, b):
            return union(to_set(a), to_set(b))


def intersect(xs, ys):
    return [(max(a, c), min(b, d))
            for (a, b) in xs for (c, d) in ys
            if max(a, c) <= min(b, d)]


def union(xs, ys):
    out = []
    for lo, hi in sorted(xs + ys):
        if out and lo <= out[-1][1] + 1:
            out[-1] = (out[-1][0], max(out[-1][1], hi))
        else:
            out.append((lo, hi))
    return out


def subset(xs, ys) -> bool:
    return all(any(c <= a and b <= d for c, d in ys) for a, b in xs)


# types

@dataclass(frozen=True)
class IntT:
    pred: Pred = TT()

    def __str__(self):
        return "{v:Int | " + fmt(self.pred) + "}"


def fmt(p):
    match p:
        case TT():
            return "⊤"
        case FF():
            return "⊥"
        case GT(n):
            return f"v > {n}"
        case GE(n):
            return f"v ≥ {n}"
        case LT(n):
            return f"v < {n}"
        case LE(n):
            return f"v ≤ {n}"
        case EQ(n):
            return f"v = {n}"
        case NE(n):
            return f"v ≠ {n}"
        case And(a, b):
            return f"({fmt(a)} ∧ {fmt(b)})"
        case Or(a, b):
            return f"({fmt(a)} ∨ {fmt(b)})"


def sub(t1: IntT, t2: IntT) -> bool:
    """t1 <: t2  iff  ⟦t1.pred⟧ ⊆ ⟦t2.pred⟧."""
    return subset(to_set(t1.pred), to_set(t2.pred))


# demo

if __name__ == "__main__":
    nonzero  = IntT(NE(0))
    positive = IntT(GT(0))
    any_int  = IntT(TT())

    # div : Int -> {v:Int | v ≠ 0} -> Int
    print(f"{positive} <: {nonzero}?", sub(positive, nonzero))       # True
    print(f"{any_int}  <: {nonzero}?", sub(any_int,  nonzero))       # False
    print(f"{IntT(EQ(0))} <: {nonzero}?", sub(IntT(EQ(0)), nonzero)) # False
    print(f"{IntT(EQ(5))} <: {nonzero}?", sub(IntT(EQ(5)), nonzero)) # True
