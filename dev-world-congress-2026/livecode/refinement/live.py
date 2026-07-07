"""A refinement type checker."""

from dataclasses import dataclass

INF = float("inf")

# Refinement types: a base type carrying a predicate on its value v
@dataclass(frozen=True)
class Int: pass                # v : Int
@dataclass(frozen=True)
class Eq: n: int               # v = n
@dataclass(frozen=True)
class Ne: n: int               # v ≠ n
@dataclass(frozen=True)
class Gt: n: int               # v > n
@dataclass(frozen=True)
class Lt: n: int               # v < n

# A tiny expression language
@dataclass(frozen=True)
class Lit:  n: int
@dataclass(frozen=True)
class Var:  name: str
@dataclass(frozen=True)
class Call: fn: str; args: tuple

SIGS = {                       # fn : (parameter types) -> result type
    "div": ((Int(), Ne(0)), Int()),
}

def values(t):                 # the integers the type admits
    match t:
        case Int(): return [(-INF, INF)]
        case Eq(n): return [(n, n)]
        case Ne(n): return [(-INF, n - 1), (n + 1, INF)]
        case Gt(n): return [(n + 1, INF)]
        case Lt(n): return [(-INF, n - 1)]

def subtype(s, t):
    ...

def infer(ctx, e):
    ...

# --- this is all for testing and printing

def pretty(e):
    match e:
        case Lit(n):         return str(n)
        case Var(x):         return x
        case Call(fn, args): return f"{fn}({', '.join(pretty(a) for a in args)})"

def show(t):
    match t:
        case Int(): return "Int"
        case Eq(n): return f"{{v = {n}}}"
        case Ne(n): return f"{{v ≠ {n}}}"
        case Gt(n): return f"{{v > {n}}}"
        case Lt(n): return f"{{v < {n}}}"

if __name__ == "__main__":
    print("div : (Int, {v ≠ 0}) → Int\n")
    ctx = {"x": Gt(0), "n": Int()}
    for e in [Call("div", (Lit(10), Lit(2))),
              Call("div", (Lit(10), Lit(0))),
              Call("div", (Lit(10), Var("x"))),
              Call("div", (Lit(10), Var("n")))]:
        try:
            print(f"  {pretty(e):14}  :  {show(infer(ctx, e))}")
        except TypeError as err:
            print(f"  {pretty(e):14}  :  TYPE ERROR   {err}")
