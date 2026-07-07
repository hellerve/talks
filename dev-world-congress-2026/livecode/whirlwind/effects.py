"""
a simple effect system.

a function type carries the effects it may perform, and those effects flow
through application. calling `f : A -> B ! {io}` in a context that forbids `io`
is a type error.

real systems (koka, eff, unison, links) support effect polymorphism,
handlers, and the handler continuations that discharge effects. this toy
tracks a fixed set of effect labels and checks that a call's effects are
permitted by its context. the characteristic move is that the effect row on
the arrow flows out to the call site (see below if that was a bit much!).
"""

from dataclasses import dataclass
from typing import Union

# base types and effectful function types

@dataclass(frozen=True)
class Base:
    name: str # e.g. Int, Str, Path


@dataclass(frozen=True)
class Fn:
    arg: "Ty"
    ret: "Ty"
    effects: frozenset # the effect row:  A -> B ! E


Ty = Union[Base, Fn]


# expressions


@dataclass(frozen=True)
class Var:
    name: str


@dataclass(frozen=True)
class App:
    fn: "Expr"
    arg: "Expr" # a call


Expr = Union[Var, App]


# here’s the magic: effects flow through application
# infer returns (<type>, <the effects the expression performs>)

def infer(ctx, e) -> tuple:
    match e:
        case Var(x):
            return ctx[x], frozenset() # a variable performs nothing
        case App(f, a):
            fty, fe = infer(ctx, f)
            aty, ae = infer(ctx, a)
            if not isinstance(fty, Fn):
                raise TypeError(f"{show(fty)} is not callable")
            if aty != fty.arg:
                raise TypeError(f"argument {show(aty)} != parameter {show(fty.arg)}")
            # the arrow's own effect row flows out, joined with the subexprs'
            return fty.ret, fe | ae | fty.effects
        case _:
            raise TypeError(f"not an expression: {e!r}")


def check_pure(ctx, e) -> Ty:
    ty, eff = infer(ctx, e)
    if eff:
        raise TypeError(f"effects {set(eff)} not allowed in a pure context")
    return ty


def show(t: Ty) -> str:
    match t:
        case Base(n):
            return n
        case Fn(a, b, e):
            return f"({show(a)} -> {show(b)}" + (f" !{set(e)}" if e else "") + ")"


# demo

if __name__ == "__main__":
    Int = Base("Int")
    Str = Base("Str")
    Path = Base("Path")
    ctx = {
        "len":      Fn(Str, Int, frozenset()),        # pure
        "readFile": Fn(Path, Str, frozenset({"io"})), # readFile : Path -> Str ! {io}
        "s":        Str,
        "p":        Path,
    }

    # len(s) is pure, and thus allowed in a pure context
    print("len(s) :", show(check_pure(ctx, App(Var("len"), Var("s")))))

    # readFile(p) performs io, and is rejected where purity is required
    try:
        check_pure(ctx, App(Var("readFile"), Var("p")))
    except TypeError as e:
        print("rejected:", e)

    # but the effect is visible in its inferred type
    ty, eff = infer(ctx, App(Var("readFile"), Var("p")))
    print(f"readFile(p) : {show(ty)} ! {set(eff)}")
